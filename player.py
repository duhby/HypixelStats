# dubs#9025
# Hypixel Stats
# 2/1/21

## If there is an "#UNSUPPORTED#" tag above a class, then that class, (and all subsequent classes),
## are not currently planned on being supported for 2.0.0s release.
## If you, or somone you know who would find any of the unsupported gamemodes useful,
## suggest it in my discord or DM me @dubs#9025.


class Player:
    class Arcade:
        class CaptureTheWool:
            # api
            def captures(player_data):
                return player_data.get('achievements').get('arcade_ctw_oh_sheep',0)

            def kills_and_assists(player_data):
                return player_data.get('achievements').get('arcade_ctw_slayer',0)


        class HypixelSays:
            # api
            def rounds(player_data):
                return player_data.get('stats').get('Arcade').get('rounds_simon_says',0)

            def wins(player_data):
                return player_data.get('stats').get('Arcade').get('wins_simon_says',0)

            # math
            def losses(player_data):
                hypixel_says = Player.Arcade.HypixelSays
                return hypixel_says.rounds(player_data) - hypixel_says.wins(player_data)

            def win_loss_ratio(player_data):
                hypixel_says = Player.Arcade.HypixelSays
                wins = hypixel_says.wins(player_data)
                losses = hypixel_says.losses(player_data)
                if losses == 0:
                    return wins
                return round(wins/losses,2)


        class PartyGames:
            # api
            def wins(player_data):
                return player_data.get('stats').get('Arcade').get('wins_party',0)

            def wins_2(player_data):
                return player_data.get('stats').get('Arcade').get('wins_party_2',0)

            def wins_3(player_data):
                return player_data.get('stats').get('Arcade').get('wins_party_3',0)

            # math
            def total_wins(player_data):
                party_games = Player.Arcade.PartyGames
                wins = party_games.wins(player_data)
                wins_2 = party_games.wins_2(player_data)
                wins_3 = party_games.wins_3(player_data)
                return wins + wins_2 + wins_3


        #UNSUPPORTED# (for the remainder of the arcade gamemodes)



    #UNSUPPORTED#
    class ArenaBrawl:
        pass



    class Bedwars:
        # api
        def level(player_data):
            return player_data.get('achievements').get('bedwars_level',0)

        def resources_collected(player_data):
            bedwars = player_data.get('stats').get('Bedwars')
            return {
                'iron':bedwars.get('iron_resources_collected_bedwars',0),
                'gold':bedwars.get('gold_resources_collected_bedwars',0),
                'diamonds':bedwars.get('diamond_resources_collected_bedwars',0),
                'emeralds':bedwars.get('emerald_resources_collected_bedwars',0)
                }

        def beds_broken(player_data):
            return player_data.get('stats').get('Bedwars').get('beds_broken_bedwars',0)

        def beds_lost(player_data):
            return player_data.get('stats').get('Bedwars').get('beds_lost_bedwars',0)

        def final_kills(player_data):
            return player_data.get('stats').get('Bedwars').get('final_kills_bedwars',0)

        def final_deaths(player_data):
            return player_data.get('stats').get('Bedwars').get('final_deaths_bedwars',0)

        def wins(player_data):
            return player_data.get('stats').get('Bedwars').get('wins_bedwars',0)

        def losses(player_data):
            return player_data.get('stats').get('Bedwars').get('losses_bedwars',0)

        def winstreak(player_data):
            return player_data.get('stats').get('Bedwars').get('winstreak',0)

        # math
        def bed_break_loss_ratio(player_data):
            bedwars = Player.Bedwars
            beds_broken = bedwars.beds_broken(player_data)
            beds_lost = bedwars.beds_lost(player_data)
            if beds_lost == 0:
                return beds_broken
            return round(beds_broken/beds_lost,1)

        def final_kill_death_ratio(player_data):
            bedwars = Player.Bedwars
            final_kills = bedwars.final_kills(player_data)
            final_deaths = bedwars.final_deaths(player_data)
            if final_deaths == 0:
                return final_kills
            return round(final_kills/final_deaths,2)

        def win_loss_ratio(player_data):
            bedwars = Player.Bedwars
            wins = bedwars.wins(player_data)
            losses = bedwars.losses(player_data)
            if losses == 0:
                return wins
            return round(wins/losses,2)


        class Solo:
            # api
            def beds_broken(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_one_beds_broken_bedwars',0)

            def beds_lost(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_one_beds_lost_bedwars',0)

            def final_kills(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_one_final_kills_bedwars',0)

            def final_deaths(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_one_final_deaths_bedwars',0)

            def wins(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_one_wins_bedwars',0)

            def losses(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_one_losses_bedwars',0)

            def winstreak(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_one_winstreak',0)

            # math
            def bed_break_loss_ratio(player_data):
                bedwars_solo = Player.Bedwars.Solo
                beds_broken = bedwars_solo.beds_broken(player_data)
                beds_lost = bedwars_solo.beds_lost(player_data)
                if beds_lost == 0:
                    return beds_broken
                return round(beds_broken/beds_lost,1)

            def final_kill_death_ratio(player_data):
                bedwars_solo = Player.Bedwars.Solo
                final_kills = bedwars_solo.final_kills(player_data)
                final_deaths = bedwars_solo.final_deaths(player_data)
                if final_deaths == 0:
                    return final_kills
                return round(final_kills/final_deaths,2)

            def win_loss_ratio(player_data):
                bedwars_solo = Player.Bedwars.Solo
                wins = bedwars_solo.wins(player_data)
                losses = bedwars_solo.losses(player_data)
                if losses == 0:
                    return wins
                return round(wins/losses,2)


        class Doubles:
            # api
            def beds_broken(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_two_beds_broken_bedwars',0)

            def beds_lost(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_two_beds_lost_bedwars',0)

            def final_kills(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_two_final_kills_bedwars',0)

            def final_deaths(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_two_final_deaths_bedwars',0)

            def wins(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_two_wins_bedwars',0)

            def losses(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_two_losses_bedwars',0)

            def winstreak(player_data):
                return player_data.get('stats').get('Bedwars').get('eight_two_winstreak',0)

            # math
            def bed_break_loss_ratio(player_data):
                bedwars_doubles = Player.Bedwars.Doubles
                beds_broken = bedwars_doubles.beds_broken(player_data)
                beds_lost = bedwars_doubles.beds_lost(player_data)
                if beds_lost == 0:
                    return beds_broken
                return round(beds_broken/beds_lost,1)

            def final_kill_death_ratio(player_data):
                bedwars_doubles = Player.Bedwars.Doubles
                final_kills = bedwars_doubles.final_kills(player_data)
                final_deaths = bedwars_doubles.final_deaths(player_data)
                if final_deaths == 0:
                    return final_kills
                return round(final_kills/final_deaths,2)

            def win_loss_ratio(player_data):
                bedwars_doubles = Player.Bedwars.Doubles
                wins = bedwars_doubles.wins(player_data)
                losses = bedwars_doubles.losses(player_data)
                if losses == 0:
                    return wins
                return round(wins/losses,2)


        class Threes:
            # api
            def beds_broken(player_data):
                return player_data.get('stats').get('Bedwars').get('four_three_beds_broken_bedwars',0)

            def beds_lost(player_data):
                return player_data.get('stats').get('Bedwars').get('four_three_beds_lost_bedwars',0)

            def final_kills(player_data):
                return player_data.get('stats').get('Bedwars').get('four_three_final_kills_bedwars',0)

            def final_deaths(player_data):
                return player_data.get('stats').get('Bedwars').get('four_three_final_deaths_bedwars',0)

            def wins(player_data):
                return player_data.get('stats').get('Bedwars').get('four_three_wins_bedwars',0)

            def losses(player_data):
                return player_data.get('stats').get('Bedwars').get('four_three_losses_bedwars',0)

            def winstreak(player_data):
                return player_data.get('stats').get('Bedwars').get('four_three_winstreak',0)

            # math
            def bed_break_loss_ratio(player_data):
                bedwars_threes = Player.Bedwars.Threes
                beds_broken = bedwars_threes.beds_broken(player_data)
                beds_lost = bedwars_threes.beds_lost(player_data)
                if beds_lost == 0:
                    return beds_broken
                return round(beds_broken/beds_lost,1)

            def final_kill_death_ratio(player_data):
                bedwars_threes = Player.Bedwars.Threes
                final_kills = bedwars_threes.final_kills(player_data)
                final_deaths = bedwars_threes.final_deaths(player_data)
                if final_deaths == 0:
                    return final_kills
                return round(final_kills/final_deaths,2)

            def win_loss_ratio(player_data):
                bedwars_threes = Player.Bedwars.Threes
                wins = bedwars_threes.wins(player_data)
                losses = bedwars_threes.losses(player_data)
                if losses == 0:
                    return wins
                return round(wins/losses,2)


        class Fours:
            # api
            def beds_broken(player_data):
                return player_data.get('stats').get('Bedwars').get('four_four_beds_broken_bedwars',0)

            def beds_lost(player_data):
                return player_data.get('stats').get('Bedwars').get('four_four_beds_lost_bedwars',0)

            def final_kills(player_data):
                return player_data.get('stats').get('Bedwars').get('four_four_final_kills_bedwars',0)

            def final_deaths(player_data):
                return player_data.get('stats').get('Bedwars').get('four_four_final_deaths_bedwars',0)

            def wins(player_data):
                return player_data.get('stats').get('Bedwars').get('four_four_wins_bedwars',0)

            def losses(player_data):
                return player_data.get('stats').get('Bedwars').get('four_four_losses_bedwars',0)

            def winstreak(player_data):
                return player_data.get('stats').get('Bedwars').get('four_four_winstreak',0)

            # math
            def bed_break_loss_ratio(player_data):
                bedwars_fours = Player.Bedwars.Fours
                beds_broken = bedwars_fours.beds_broken(player_data)
                beds_lost = bedwars_fours.beds_lost(player_data)
                if beds_lost == 0:
                    return beds_broken
                return round(beds_broken/beds_lost,1)

            def final_kill_death_ratio(player_data):
                bedwars_fours = Player.Bedwars.Fours
                final_kills = bedwars_fours.final_kills(player_data)
                final_deaths = bedwars_fours.final_deaths(player_data)
                if final_deaths == 0:
                    return final_kills
                return round(final_kills/final_deaths,2)

            def win_loss_ratio(player_data):
                bedwars_fours = Player.Bedwars.Fours
                wins = bedwars_fours.wins(player_data)
                losses = bedwars_fours.losses(player_data)
                if losses == 0:
                    return wins
                return round(wins/losses,2)


        class Teams:
            # api
            def beds_broken(player_data):
                return player_data.get('stats').get('Bedwars').get('two_four_beds_broken_bedwars',0)

            def beds_lost(player_data):
                return player_data.get('stats').get('Bedwars').get('two_four_beds_lost_bedwars',0)

            def final_kills(player_data):
                return player_data.get('stats').get('Bedwars').get('two_four_final_kills_bedwars',0)

            def final_deaths(player_data):
                return player_data.get('stats').get('Bedwars').get('two_four_final_deaths_bedwars',0)

            def wins(player_data):
                return player_data.get('stats').get('Bedwars').get('two_four_wins_bedwars',0)

            def losses(player_data):
                return player_data.get('stats').get('Bedwars').get('two_four_losses_bedwars',0)

            def winstreak(player_data):
                return player_data.get('stats').get('Bedwars').get('two_four_winstreak',0)

            # math
            def bed_break_loss_ratio(player_data):
                bedwars_two_four = Player.Bedwars.TwoFour
                beds_broken = bedwars_two_four.beds_broken(player_data)
                beds_lost = bedwars_two_four.beds_lost(player_data)
                if beds_lost == 0:
                    return beds_broken
                return round(beds_broken/beds_lost,1)

            def final_kill_death_ratio(player_data):
                bedwars_two_four = Player.Bedwars.Fours.TwoFour
                final_kills = bedwars_two_four.final_kills(player_data)
                final_deaths = bedwars_two_four.final_deaths(player_data)
                if final_deaths == 0:
                    return final_kills
                return round(final_kills/final_deaths,2)

            def win_loss_ratio(player_data):
                bedwars_two_four = Player.Bedwars.Fours.TwoFour
                wins = bedwars_two_four.wins(player_data)
                losses = bedwars_two_four.losses(player_data)
                if losses == 0:
                    return wins
                return round(wins/losses,2)


        #UNSUPPORTED#
        class Dreams:
            class Armed:
                pass


            class Castle:
                pass


            class Lucky:
                pass


            class Rush:
                pass


            class Ultimate:
                pass


            class Voidless:
                pass



    #UNSUPPORTED#
    class Blitz:
        pass



    #UNSUPPORTED#
    class BuildBattle:
        pass



    #UNSUPPORTED#
    class CopsAndCrims:
        pass



    #UNSUPPORTED#
    class CrazyWalls:
        pass



    class Duels:
        class Blitz:
            pass


        class Bow:
            pass


        class Bridge:
            pass


        class Classic:
            pass


        class NoDebuff:
            pass


        class OP:
            pass


        class Skywars:
            pass


        class Sumo:
            pass


        class UHC:
            pass



    class MegaWalls:
        pass



    class MurderMystery:
        class classic:
            pass


        #UNSUPPORTED#
        class Assassins:
            pass


        #UNSUPPORTED#
        class DoubleUp:
            pass


        #UNSUPPORTED#
        class Infection:
            pass



    #UNSUPPORTED#
    class Paintball:
        pass



    #UNSUPPORTED#
    class Quake:
        pass



    #UNSUPPORTED#
    class Skyclash:
        pass



    class Skywars:
        class ranked:
            pass


        class SoloNormal:
            pass


        class SoloInsane:
            pass


        class TeamNormal:
            pass


        class TeamInsane:
            pass



    #UNSUPPORTED#
    class SmashHeroes:
        pass



    #UNSUPPORTED#
    class SpeedUHC:
        pass



    class TurboKartRacers:
        pass



    class TntGames:
        class tntRun:
            pass


        #UNSUPPORTED#
        class PvpRun:
            pass


        class TntTag:
            pass


        #UNSUPPORTED#
        class BowSpleef:
            pass


        #UNSUPPORTED#
        class Wizards:
            pass



    class UHC:
        class Solo:
            pass


        #UNSUPPORTED#
        class Team:
            pass



    #UNSUPPORTED#
    class VampireZ:
        pass



    #UNSUPPORTED#
    class Walls:
        pass



    #UNSUPPORTED#
    class WarLords:
        pass
