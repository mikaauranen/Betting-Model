# SÄÄTÖVIVUT
DIVISOR_BO3 = 700 
DIVISOR_BO1 = 800 
SKILL_MULTIPLIER = 500

def get_adjusted_elo_from_ratings(base_elo, ratings):
    """
    Uusi versio: Laskee Adjusted ELO:n suoraan pelaajien rating-listan perusteella.
    'ratings' on lista lukuja, esim: [1.12, 1.05, 1.20, 0.98, 1.02]
    """
    if not ratings:
        return base_elo, 1.00 # Jos ei pelaajia, palautetaan base ELO ja 1.00 rating
    
    average_rating = sum(ratings) / len(ratings)

    # Lasketaan bonus: (Rating - 1.00) * 500
    skill_modifier = (average_rating - 1.00) * SKILL_MULTIPLIER
    adjusted_elo = base_elo + skill_modifier

    return adjusted_elo, average_rating

def calculate_win_probability(elo_a, elo_b, is_bo1=False):
    """Laskee todennäköisyyden Adjusted ELO -kaavalla."""
    divisor = DIVISOR_BO1 if is_bo1 else DIVISOR_BO3
    elo_difference = elo_b - elo_a
    
    # ELO-todennäköisyyskaava
    probability_a = 1 / (1 + 10 ** (elo_difference / divisor))
    return probability_a

def calculate_kelly_bet(probability, offered_odds, fraction=0.25):
    """Laskee Kelly-kriteerin mukaisen panossuosituksen."""
    if probability <= 0 or offered_odds <= 1.0: 
        return 0.0
        
    q = 1 - probability
    b = offered_odds - 1 
    f_star = ((b * probability) - q) / b
    
    return max(0.0, f_star * fraction) * 100