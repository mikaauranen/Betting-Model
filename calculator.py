DIVISOR_BO3 = 700 
DIVISOR_BO1 = 800 
SKILL_MULTIPLIER = 500
FORM_K_FACTOR = 30  # Määrittää, kuinka aggressiivisesti 3kk ottelut vaikuttavat ELOon

def get_adjusted_elo_from_ratings(base_elo, ratings):
    if not ratings:
        return base_elo, 1.00
    average_rating = sum(ratings) / len(ratings)
    skill_modifier = (average_rating - 1.00) * SKILL_MULTIPLIER
    return base_elo + skill_modifier, average_rating

def calculate_win_probability(elo_a, elo_b, is_bo1=False):
    divisor = DIVISOR_BO1 if is_bo1 else DIVISOR_BO3
    elo_difference = elo_b - elo_a
    probability_a = 1 / (1 + 10 ** (elo_difference / divisor))
    return probability_a

def calculate_form_bonus(team_id, recent_matches):
    """
    Laskee kuntobonuksen (Form Factor) otteluhistorian perusteella.
    Odotusarvo lasketaan vastustajan ELO-luvun mukaan.
    """
    if not recent_matches:
        return 0.0

    total_form_modifier = 0.0

    for match in recent_matches:
        home_id, away_id, home_score, away_score, home_elo, away_elo, _, _ = match
        
        # Katsotaan, oliko tutkittava joukkue kotona vai vieraissa
        if team_id == home_id:
            my_elo = home_elo
            opp_elo = away_elo
            actual_outcome = 1.0 if home_score > away_score else 0.0
        else:
            my_elo = away_elo
            opp_elo = home_elo
            actual_outcome = 1.0 if away_score > home_score else 0.0

        if home_score == away_score:
            actual_outcome = 0.5  # Tasapeli (jos käytössä)

        # Lasketaan matsin odotusarvo ennen peliä
        elo_diff = opp_elo - my_elo
        expected_outcome = 1 / (1 + 10 ** (elo_diff / 700))

        # ELO-päivityskaava: K * (Tulos - Odotus)
        match_modifier = FORM_K_FACTOR * (actual_outcome - expected_outcome)
        total_form_modifier += match_modifier

    return total_form_modifier

def calculate_kelly_bet(probability, offered_odds, fraction=0.25):
    if probability <= 0 or offered_odds <= 1.0: 
        return 0.0
    q = 1 - probability
    b = offered_odds - 1 
    f_star = ((b * probability) - q) / b
    return max(0.0, f_star * fraction) * 100