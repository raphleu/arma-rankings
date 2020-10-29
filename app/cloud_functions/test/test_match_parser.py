import unittest
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../functions')
import match_parser

class TestMatchLogParse(unittest.TestCase):
    def test_parse_tst_log_file(self):
        expected_return = [
            {
                'name': "pickup-tst1.2020-08-14.19:22:56", 
                'match_winner': 'team_orange',
                'teams': {
                    'team_gold': {
                        'players': [
                            {
                                'username': 'Carnage@forums',
                                'score': '510'    
                            }, 
                            {
                                'username': 'Jericho@forums',
                                'score': '360'
                            }
                        ], 
                        'score': '1725'
                    }, 
                    'team_purple': {
                        'players': [
                            {
                                'username': 'fulcrum@forums',
                                'score': '180'
                            },
                            {
                                'username': 'ClundXIII@forums',
                                'score': '120'
                            }
                        ],
                        'score': '400' 
                    }, 
                    'team_ugly': {
                        'players': [
                            {
                                'username': 'Agility@forums',
                                'score': '390'
                            }, 
                            {
                                'username': '.Lightning@forums',
                                'score': '120'
                            }
                        ],
                        'score': '910'
                    },
                    'team_orange': {
                        'players': [
                            {
                                'username': 'misterplayer@forums', 
                                'score': '690'
                            }, 
                            {
                                'username': 'dooov@forums',
                                'score': '270'
                            }
                        ], 
                        'score': '2005'
                    }
                }, 
                'time': '19:22:56',
                'date': '2020-08-14', 
                'matchtype': 'pickup-tst1'
            }
        ]
        with open('test_tst_data.txt', 'r') as file:
            data = file.read()
        parsed_data = match_parser.parse_match_log(data, 2000, 'pickup-tst1')
        self.assertItemsEqual(parsed_data, expected_return)
    def test_parse_tst_log_file_people_leaving_before_end(self):
        self.maxDiff = None
        expected_return = [
            {
                'name': "pickup-tst1.2020-08-14.19:22:56", 
                'match_winner': 'team_orange',
                'teams': {
                    'team_gold': {
                        'players': [
                            {
                                'username': 'Carnage@forums',
                                'score': '510'    
                            }, 
                            {
                                'username': 'Jericho@forums',
                                'score': '-1'
                            }
                        ], 
                        'score': '1725'
                    }, 
                    'team_purple': {
                        'players': [
                            {
                                'username': 'fulcrum@forums',
                                'score': '180'
                            },
                            {
                                'username': 'ClundXIII@forums',
                                'score': '120'
                            }
                        ],
                        'score': '400' 
                    }, 
                    'team_ugly': {
                        'players': [
                            {
                                'username': '.Lightning@forums',
                                'score': '-1'
                            },
                            {
                                'username': 'Agility@forums',
                                'score': '-1'
                            }
                        ],
                        'score': '910'
                    },
                    'team_orange': {
                        'players': [
                            {
                                'username': 'misterplayer@forums', 
                                'score': '690'
                            }, 
                            {
                                'username': 'dooov@forums',
                                'score': '270'
                            }
                        ], 
                        'score': '2005'
                    }
                }, 
                'time': '19:22:56',
                'date': '2020-08-14', 
                'matchtype': 'pickup-tst1'
            }
        ]
        with open('test_tst_data_people_leaving.txt', 'r') as file:
            data = file.read()
        parsed_data = match_parser.parse_match_log(data, 200, 'pickup-tst1')
        self.assertItemsEqual(parsed_data, expected_return)

    def test_parse_tst_all_players_left_a_team(self):
        expected_return = [
            {
                "name": "pickup-tst1.2020-08-16.16:19:13",
                "match_winner": "team_purple",
                "teams": {
                "team_gold": {
                    "players": [
                    {
                        "username": "thxmp@forums",
                        "score": "-1"
                    },
                    {
                        "username": "misterplayer@forums",
                        "score": "-1"
                    }
                    ],
                    "score": "-1"
                },
                "team_purple": {
                    "players": [
                    {
                        "username": "Titanoboa@forums",
                        "score": "510"
                    },
                    {
                        "username": "raph123@forums",
                        "score": "450"
                    }
                    ],
                    "score": "2050"
                },
                "team_ugly": {
                    "players": [
                    {
                        "username": "Moonlight@forums",
                        "score": "420"
                    },
                    {
                        "username": "syllabear@forums",
                        "score": "330"
                    }
                    ],
                    "score": "1070"
                },
                "team_orange": {
                    "players": [
                    {
                        "username": "Desolate@forums",
                        "score": "-1"
                    },
                    {
                        "username": "RoterBaron1337@forums",
                        "score": "-1"
                    }
                    ],
                    "score": "-1"
                }
                },
                "time": "16:19:13",
                "date": "2020-08-16",
                "matchtype": "pickup-tst1"
            }
        ]
        with open('test_tst_all_players_left_a_team.txt', 'r') as file:
            data = file.read()
        parsed_data = match_parser.parse_match_log(data, 200, 'pickup-tst1')
        self.assertItemsEqual(parsed_data, expected_return)

    def test_parse_fort_log_file(self):
        expected_return = [
            {
                "match_winner": "team_gold",
                "teams": {
                "team_blue": {
                    "players": [
                    {
                        "username": "johnny.nbk.@forums",
                        "score": "22"
                    },
                    {
                        "username": "F0RC3@forums",
                        "score": "18"
                    },
                    {
                        "username": "kite@forums",
                        "score": "14"
                    },
                    {
                        "username": "Agility@forums",
                        "score": "10"
                    },
                    {
                        "username": "smurf@lt",
                        "score": "6"
                    },
                    {
                        "username": "Moonlight@forums",
                        "score": "6"
                    }
                    ],
                    "score": "96"
                },
                "team_gold": {
                    "players": [
                    {
                        "username": "vov@forums",
                        "score": "26"
                    },
                    {
                        "username": "syllabear@forums",
                        "score": "16"
                    },
                    {
                        "username": "woof@forums",
                        "score": "12"
                    },
                    {
                        "username": "DaGarBBaGeMAN@forums",
                        "score": "12"
                    },
                    {
                        "username": "Jericho@forums",
                        "score": "12"
                    },
                    {
                        "username": "breeze@forums",
                        "score": "6"
                    }
                    ],
                    "score": "202"
                }
                },
                "date": "2020-10-26",
                "time": "20:56:49",
                "matchtype": "pickup-fortress1",
                "name": "pickup-fortress1.2020-10-26.20:56:49"
            }
        ]
        with open('test_fort_data.txt', 'r') as file:
            data = file.read()
        parsed_data = match_parser.parse_match_log(data, 200, 'pickup-fortress1')
        self.assertItemsEqual(parsed_data, expected_return)

if __name__ == '__main__':
    unittest.main()