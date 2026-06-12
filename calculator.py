# SÄÄTÖVIVUT (Näitä muuttamalla mallin jyrkkyys muuttuu)
DIVISOR_BO3 = 700  # Loivennettu: Maksimisuosikin kerroin asettuu realistiseen ~1.10 - 1.15 väliin
DIVISOR_BO1 = 800  # BO1 on vielä herkempi yllätyksille

SKILL_MULTIPLIER = 500 # Pidetään tämä samana, se antaa juuri sopivan tulivoimabonuksen

def get_adjusted_elo(base_elo, roster, players_db):
    """
    Laskee joukkueen 'Adjusted ELO:n' pelaajien nykykunnon perusteella.
    """
    if not roster:
        return base_elo, 0.0

    ratings = []
    for player in roster:
        player_rating = players_db.get(player, {}).get("rating", 1.00)
        ratings.append(player_rating)
    
    average_rating = sum(ratings) / len(ratings)

    # Lasketaan bonus: esim. (1.15 - 1.00) * 500 = +75
    skill_modifier = (average_rating - 1.00) * SKILL_MULTIPLIER
    adjusted_elo = base_elo + skill_modifier

    return adjusted_elo, average_rating

def calculate_win_probability(elo_a, elo_b, is_bo1=False):
    """
    Laskee todennäköisyyden Adjusted ELO -kaavalla.
    """
    divisor = DIVISOR_BO1 if is_bo1 else DIVISOR_BO3
    elo_difference = elo_b - elo_a
    
    probability_a = 1 / (1 + 10 ** (elo_difference / divisor))
    return probability_a

def calculate_kelly_bet(probability, offered_odds, fraction=0.25):
    """
    Laskee Kelly-kriteerin mukaisen panossuosituksen.
    """
    if probability <= 0 or offered_odds <= 1.0: 
        return 0.0
        
    q = 1 - probability
    b = offered_odds - 1 
    f_star = ((b * probability) - q) / b
    
    return max(0.0, f_star * fraction) * 100