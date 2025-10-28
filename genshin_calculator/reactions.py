

LVL90_MULTIPLICATOR = 1446.85

class Reaction():
    """Base class for elemental reactions.

    Attributes
    ----------
    multiplicator : float
        The base multiplier for the reaction.
    """

    def __init__(self, multiplicator):
        self.multiplicator = multiplicator
    
    def __call__(self, dmg: float, em: float, reaction_bonus: float) -> float:
        raise NotImplementedError


class AdditiveReaction(Reaction):
    """Class for additive elemental reactions."""

    def __call__(self, dmg: float, em: float, reaction_bonus: float) -> float:
        """Apply the additive reaction to the damage.

        Parameters
        ----------
        dmg : float
            The base damage.
        em : float
            The elemental mastery of the character.
        reaction_bonus : float
            Additional reaction bonus.

        Returns
        -------
        float
            The modified damage after applying the additive reaction.
        """
        return dmg + 16 * self.multiplicator * LVL90_MULTIPLICATOR * (1 + em / (em + 2000) + reaction_bonus)
    

class MutltiplicativeReaction(Reaction):
    """Class for multiplicative elemental reactions."""

    def __call__(self, dmg: float, em: float, reaction_bonus: float) -> float:
        """Apply the multiplicative reaction to the damage.

        Parameters
        ----------
        dmg : float
            The base damage.
        em : float
            The elemental mastery of the character.
        reaction_bonus : float
            Additional reaction bonus.

        Returns
        -------
        float
            The modified damage after applying the multiplicative reaction.
        """
        return self.multiplicator * dmg * (1 + reaction_bonus + 2.78 * em / (1400 + em))

# TODO : check values
NO_REACTIONS = AdditiveReaction(0)

BURNING = AdditiveReaction(0.25)
SUPERCONDUCT = AdditiveReaction(0.5)
SWIRL = AdditiveReaction(0.6)
ELECTRO_CHARGED = AdditiveReaction(1.2)
SHATTERED = AdditiveReaction(1.5)
OVERLOAD = AdditiveReaction(2.0)

FORWARD_MELT = MutltiplicativeReaction(2)
FORWARD_VAPORIZE = MutltiplicativeReaction(2)
REVERSE_MELT = MutltiplicativeReaction(1.5)
REVERSE_VAPORIZE = MutltiplicativeReaction(1.5)