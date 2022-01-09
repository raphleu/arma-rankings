schedule_for_us = [
    {
        'day': 'Thursdays',
        'utc_time': '00:00'
    },
    {
        'day': 'Saturdays',
        'utc_time': '21:00'
    },
]

schedule_for_eu = [
    {
        'day': 'Tuesdays',
        'utc_time': '19:00'
    },
    {
        'day': 'Saturdays',
        'utc_time': '19:00'
    },
]

match_types = {
    'leagues': {
        'All time': {
            'sbl-s2': {
                'header': 'SBL',
                'title': 'Sumo Bar League',
                'match_subtype_id': 'sbl-s2',
                'description': 'Public, ranked sumobar matches, hosted on US and EU servers! Open to anyone, see <a href="/league-info?match_subtype_id=sbl-s2">League Info</a> for how to join. Can you make it to the top?',
                'banner_image': 'titan_banner2_trimmed.png',
                'text_image': 'sbls2text.png'
            }
        }
    },
    'pickup': {
        'Live (last 90 days)': {
            'pickup-tst1_live': {
                'header': 'TST',
                'title': 'TST pickup',
                'match_subtype_id': 'pickup-tst1_live',
                'description': 'Pickup TST! Competitive 2v2v2v2 sumo gameplay. Sign up on discord in the #pickup channel! Rankings here reflect the past 90 days of gameplay.',
                'banner_image': 'titan_banner1_trimmed.png',
                'text_image': 'tstpickuptextlive.png',
                'about': 'The ratings here are calculated using an algorithm called Trueskill, invented by microsoft for multiplayer games and reflect the past 90 days of gameplay. Trueskill has many factors that go into it and can be tuned. For example, Trueskill takes into account the strength of your opposing team, so two players with the same number of wins and losses can have different ratings (a loss to a high rated team means less of a hit to your rating than one to a weaker team). Individual score does not matter, purely winning or losing and who you are against. More info can be found <a href="https://trueskill.org/">here</a>. I have tried tuning parameters to work best for this gametype, but if you have suggestions for how they can be improved, please let me (raph) know.',
                'type': 'Live (last 90 days)',
            },
            'pickup-fortress2_live': {
                'header': 'Fort',
                'title': 'Fortress pickup',
                'match_subtype_id': 'pickup-fortress2_live',
                'description': 'Pickup fortress! Competitive 6v6 gameplay. Sign up on discord in the #pickup channel! Rankings here reflect the past 90 days of gameplay.',
                'banner_image': 'titan_banner2_trimmed.png',
                'text_image': 'fortpickuptextlive.png',
                'about': 'The ratings here are calculated using an algorithm called Trueskill, invented by microsoft for multiplayer games and reflect the past 90 days of gameplay. Trueskill has many factors that go into it and can be tuned. For example, Trueskill takes into account the strength of your opposing team, so two players with the same number of wins and losses can have different ratings (a loss to a high rated team means less of a hit to your rating than one to a weaker team). Individual score does not matter, purely winning or losing and who you are against. More info can be found <a href="https://trueskill.org/">here</a>. I have tried tuning parameters to work best for this gametype, but if you have suggestions for how they can be improved, please let me (raph) know.',
                'type': 'Live (last 90 days)'
            },
        }, 
        'All time': {
            'pickup-fortress2': {
                'header': 'Fort',
                'title': 'Fortress pickup season 2',
                'match_subtype_id': 'pickup-fortress2',
                'description': 'Pickup fortress! Competitive 6v6 gameplay. Sign up on discord in the #pickup channel!',
                'banner_image': 'titan_banner2_trimmed.png',
                'text_image': 'fortpickuptext.png',
                'about': 'The ratings here are calculated using an algorithm called Trueskill, invented by microsoft for multiplayer games. Trueskill has many factors that go into it and can be tuned. For example, Trueskill takes into account the strength of your opposing team, so two players with the same number of wins and losses can have different ratings (a loss to a high rated team means less of a hit to your rating than one to a weaker team). Individual score does not matter, purely winning or losing and who you are against. More info can be found <a href="https://trueskill.org/">here</a>. I have tried tuning parameters to work best for this gametype, but if you have suggestions for how they can be improved, please let me (raph) know.',
                'type': 'All time'
            },
            'pickup-tst1': {
                'header': 'TST',
                'title': 'TST pickup',
                'match_subtype_id': 'pickup-tst1',
                'description': 'Pickup TST! Competitive 2v2v2v2 sumo gameplay. Sign up on discord in the #pickup channel!',
                'banner_image': 'titan_banner1_trimmed.png',
                'text_image': 'tstpickuptext.png',
                'about': 'The ratings here are calculated using an algorithm called Trueskill, invented by microsoft for multiplayer games. Trueskill has many factors that go into it and can be tuned. For example, Trueskill takes into account the strength of your opposing team, so two players with the same number of wins and losses can have different ratings (a loss to a high rated team means less of a hit to your rating than one to a weaker team). Individual score does not matter, purely winning or losing and who you are against. More info can be found <a href="https://trueskill.org/">here</a>. I have tried tuning parameters to work best for this gametype, but if you have suggestions for how they can be improved, please let me (raph) know.',
                'type': 'All time'
            }
        }
    },
    'archive': {
        'All time': {
            'pickup-fortress1': {
                'header': 'Fort',
                'title': 'Fortress pickup season 1',
                'match_subtype_id': 'pickup-fortress1',
                'description': 'Pickup fortress! Competitive 6v6 gameplay. Sign up on discord in the #pickup channel!',
                'banner_image': 'fort_bg2.png',
                'text_image': 'fortpickuptext.png',
                'about': 'The ratings here are calculated using an algorithm called Trueskill, invented by microsoft for multiplayer games. Trueskill has many factors that go into it and can be tuned. For example, Trueskill takes into account the strength of your opposing team, so two players with the same number of wins and losses can have different ratings (a loss to a high rated team means less of a hit to your rating than one to a weaker team). Individual score does not matter, purely winning or losing and who you are against. More info can be found <a href="https://trueskill.org/">here</a>. I have tried tuning parameters to work best for this gametype, but if you have suggestions for how they can be improved, please let me (raph) know.',
                'type': 'All time'
            },
            'sbl-us': {
                'header': 'US',
                'title': 'Sumo Bar League US',
                'match_subtype_id': 'sbl-us',
                'description': 'Public, ranked sumobar matches, hosted on US servers! Open to anyone, see <a href="/league-info?match_subtype_id=sbl-us">League Info</a> for how to join. Can you make it to the top?',
                'banner_image': 'titan_banner3_trimmed.png',
                'text_image': 'sumobarusatext.png',
                'type': 'All time'
            },
            'sbl-eu': {
                'header': 'EU',
                'title': 'Sumo Bar League EU',
                'match_subtype_id': 'sbl-eu',
                'description': 'Public, ranked sumobar matches, hosted on EU servers! Open to anyone, see <a href="/league-info?match_subtype_id=sbl-eu">League Info</a> for how to join. Can you make it to the top?',
                'banner_image': 'titan_banner1_trimmed.png', 
                'text_image': 'sumobartexteu.png',
                'type': 'All time'
            }, 
            'sbl-s2': {
                'header': 'SBL',
                'title': 'Sumo Bar League season 2',
                'match_subtype_id': 'sbl-s2',
                'description': 'Public, ranked sumobar matches, hosted on US and EU servers! Open to anyone, see <a href="/league-info?match_subtype_id=sbl-s2">League Info</a> for how to join. Can you make it to the top?',
                'banner_image': 'titan_banner2_trimmed.png',
                'text_image': 'sbls2text.png',
                'type': 'All time'
            }
        }
    }
}

match_subtype_to_type = {
    'pickup-fortress1': 'archive',
    'sbl-s2': 'archive',
    'sbl-eu': 'archive',
    'sbl-us': 'archive',
    'pickup-tst1': 'pickup',
    'pickup-tst1_live': 'pickup',
    'pickup-fortress2': 'pickup',
    'pickup-fortress2_live': 'pickup',
    'pickup-fortress-all': 'pickup'
}

live_seasons = {'pickup-tst1', 'pickup-fortress2'}