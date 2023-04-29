from unittest import TestCase
from app import app
from flask import session, jsonify
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['current_board'] = None


    def test_board_render(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                #Gives the board a pretend layout.
                change_session['current_board'] = [["A","B","C","D","E"],["F","G","H","I","J"],["L","M","N","O","P"],["Q","R","S","T","U"],["V","W","X","Y","Z"]]
                
            res = client.get('/board')
            html = res.get_data(as_text=True)
            
            #Is the board still the premade board?
            self.assertEqual(session['current_board'], [["A","B","C","D","E"],["F","G","H","I","J"],["L","M","N","O","P"],["Q","R","S","T","U"],["V","W","X","Y","Z"]])

            #Does the page load?
            self.assertEqual(res.status_code, 200)

            #Does the board render correctly?
            correct_html_table = '<table class="board_table">\n    \n    <tr class ="board_row">\n        \n        <td class="board_cell"><div class="tile">A</div></td>\n        \n        <td class="board_cell"><div class="tile">B</div></td>\n        \n        <td class="board_cell"><div class="tile">C</div></td>\n        \n        <td class="board_cell"><div class="tile">D</div></td>\n        \n        <td class="board_cell"><div class="tile">E</div></td>\n        \n    </tr>\n    \n    <tr class ="board_row">\n        \n        <td class="board_cell"><div class="tile">F</div></td>\n        \n        <td class="board_cell"><div class="tile">G</div></td>\n        \n        <td class="board_cell"><div class="tile">H</div></td>\n        \n        <td class="board_cell"><div class="tile">I</div></td>\n        \n        <td class="board_cell"><div class="tile">J</div></td>\n        \n    </tr>\n    \n    <tr class ="board_row">\n        \n        <td class="board_cell"><div class="tile">L</div></td>\n        \n        <td class="board_cell"><div class="tile">M</div></td>\n        \n        <td class="board_cell"><div class="tile">N</div></td>\n        \n        <td class="board_cell"><div class="tile">O</div></td>\n        \n        <td class="board_cell"><div class="tile">P</div></td>\n        \n    </tr>\n    \n    <tr class ="board_row">\n        \n        <td class="board_cell"><div class="tile">Q</div></td>\n        \n        <td class="board_cell"><div class="tile">R</div></td>\n        \n        <td class="board_cell"><div class="tile">S</div></td>\n        \n        <td class="board_cell"><div class="tile">T</div></td>\n        \n        <td class="board_cell"><div class="tile">U</div></td>\n        \n    </tr>\n    \n    <tr class ="board_row">\n        \n        <td class="board_cell"><div class="tile">V</div></td>\n        \n        <td class="board_cell"><div class="tile">W</div></td>\n        \n        <td class="board_cell"><div class="tile">X</div></td>\n        \n        <td class="board_cell"><div class="tile">Y</div></td>\n        \n        <td class="board_cell"><div class="tile">Z</div></td>\n        \n    </tr>\n    \n</table>'
            self.assertIn(correct_html_table, html)

    def test_board_init(self):
        with app.test_client() as client:

            res = client.get('/board')
            
            #Does the page load?
            self.assertEqual(res.status_code, 200)
            
            #Is the board data the correct type?
            self.assertIsNotNone(session['current_board'])
            self.assertIsInstance(session['current_board'], list)
            self.assertIsInstance(session['current_board'][0], list)
            self.assertIsInstance(session['current_board'][0][0], str)

            #Is the board data the correct length?
            self.assertEqual(len(session['current_board']), 5)
            self.assertEqual(len(session['current_board'][0]), 5)
            self.assertEqual(len(session['current_board'][0][0]), 1)

            with client.session_transaction() as change_session:
                #Set to invalid value
                change_session['current_board'] = 3
            
            res = client.get('/board')

            #Was new board created when presented with an invalid board?
            self.assertNotEqual(session['current_board'], 3)

            with client.session_transaction() as change_session:
                #Give the board another invalid value (one array is only 4 long).
                change_session['current_board'] = [["A","B","C","D"],["F","G","H","I","J"],["L","M","N","O","P"],["Q","R","S","T","U"],["V","W","X","Y","Z"]]

            res = client.get('/board')

            #Was new board created when presented with an invalid board?
            self.assertNotEqual(session['current_board'], [["A","B","C","D"],["F","G","H","I","J"],["L","M","N","O","P"],["Q","R","S","T","U"],["V","W","X","Y","Z"]])    

    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')
            self.assertEqual(res.status_code, 200)

    def test_guess_request(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                #Give the board a pretend layout again.
                change_session['current_board'] = [["A","B","C","D","E"],["F","G","H","I","J"],["L","M","N","O","P"],["Q","R","S","T","U"],["V","W","X","Y","Z"]]
            
            res = client.post('/submit', data={'guess': 'hide'})

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_json(),  jsonify({'result':'ok'}).get_json())

            res = client.post('/submit', data={'guess': 'cock'})

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_json(),  jsonify({'result':'not-on-board'}).get_json())

            res = client.post('/submit', data={'guess': 'asfgb'})

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.get_json(),  jsonify({'result':'not-word'}).get_json())



            

                

            



