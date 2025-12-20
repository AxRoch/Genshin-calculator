from .data import TRANSFORMATIVE_REACTION_MULTIPLIERS


class Reaction():
    """Base class for elemental reactions.

    Attributes
    ----------
    multiplicator : float
        The base multiplier for the reaction.
    """

    def __init__(self, multiplicator):
        self.multiplicator = multiplicator
    
    def __call__(self, dmg: float, em: float, reaction_bonus: float, char_lvl: int) -> float:
        raise NotImplementedError


class TransformativeReaction(Reaction):
    """Class for additive elemental reactions."""

    def __call__(self, dmg: float, em: float, reaction_bonus: float, char_lvl: int) -> float:
        """Apply the additive reaction to the damage.

        Parameters
        ----------
        dmg : float
            The base damage.
        em : float
            The elemental mastery of the character.
        reaction_bonus : float
            Additional reaction bonus.
        char_lvl : int
            The level of the character performing the reaction.

        Returns
        -------
        float
            The modified damage after applying the additive reaction.
        """
        lvl_multiplier = TRANSFORMATIVE_REACTION_MULTIPLIERS[char_lvl]
        return dmg + self.multiplicator * lvl_multiplier * (1 + 16 * em / (em + 2000) + reaction_bonus / 100)
    

class MutltiplicativeReaction(Reaction):
    """Class for multiplicative elemental reactions."""

    def __call__(self, dmg: float, em: float, reaction_bonus: float, char_lvl: int = None) -> float:
        """Apply the multiplicative reaction to the damage.

        Parameters
        ----------
        dmg : float
            The base damage.
        em : float
            The elemental mastery of the character.
        reaction_bonus : float
            Additional reaction bonus.
        char_lvl : int, optional
            The level of the character performing the reaction.
            This value does not affect multiplicative reaction but this argument is let to remain coherent with
            transformative reactions.

        Returns
        -------
        float
            The modified damage after applying the multiplicative reaction.
        """
        return self.multiplicator * dmg * (1 + reaction_bonus / 100 + 2.78 * em / (1400 + em))

# TODO : check values
NO_REACTIONS = TransformativeReaction(0)

BURNING = TransformativeReaction(0.25)
SUPERCONDUCT = TransformativeReaction(0.5)
SWIRL = TransformativeReaction(0.6)
ELECTRO_CHARGED = TransformativeReaction(1.2)
SHATTERED = TransformativeReaction(1.5)
OVERLOAD = TransformativeReaction(2.0)

FORWARD_MELT = MutltiplicativeReaction(2)
FORWARD_VAPORIZE = MutltiplicativeReaction(2)
REVERSE_MELT = MutltiplicativeReaction(1.5)
REVERSE_VAPORIZE = MutltiplicativeReaction(1.5)