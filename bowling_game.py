class BowlingGame:
    def __init__(self):
        """
        Initialize a new bowling game.
        
        Creates empty rolls list and sets current roll index to 0.
        Each game consists of 10 frames with specific scoring rules.
        """
        self.rolls = []
        self.current_roll = 0

    def roll(self, pins):
        """
        Record a roll in the game.

        Args:
            pins (int): Number of pins knocked down in this roll (0-10)
            
        Raises:
            ValueError: If pins is not between 0 and 10 inclusive
        """
        if not isinstance(pins, int) or pins < 0 or pins > 10:
            raise ValueError(f"Invalid pin count: {pins}. Must be integer between 0 and 10.")
            
        self.rolls.append(pins)
        self.current_roll += 1

    def score(self):
        """
        Calculate the total score for the current game.
        
        Implements standard ten-pin bowling scoring rules:
        - Strike: 10 + next 2 rolls
        - Spare: 10 + next 1 roll  
        - Open frame: sum of 2 rolls
        - Tenth frame: special rules for strikes/spares
        """
        score = 0
        frame_index = 0

        # First 9 frames
        for frame in range(9):
            if self._is_strike(frame_index):
                score += 10 + self._strike_bonus(frame_index)
                frame_index += 1
            elif self._is_spare(frame_index):
                score += 10 + self._spare_bonus(frame_index)
                frame_index += 2
            else:
                score += self.rolls[frame_index] + self.rolls[frame_index + 1]
                frame_index += 2

        # 10th frame
        score += self._score_tenth_frame(frame_index)
        return score

    def _score_tenth_frame(self, frame_index):
        """Calculate score for the tenth frame with special rules."""
        if self._is_strike(frame_index):
            if frame_index + 2 < len(self.rolls):
                return 10 + self.rolls[frame_index + 1] + self.rolls[frame_index + 2]
            elif frame_index + 1 < len(self.rolls):
                return 10 + self.rolls[frame_index + 1]
            else:
                return 10
        elif self._is_spare(frame_index):
            if frame_index + 2 < len(self.rolls):
                return 10 + self.rolls[frame_index + 2]
            else:
                return 10
        else:
            if frame_index + 1 < len(self.rolls):
                return self.rolls[frame_index] + self.rolls[frame_index + 1]
            elif frame_index < len(self.rolls):
                return self.rolls[frame_index]
            else:
                return 0

    def _is_strike(self, frame_index):
        """Check if the roll at frame_index is a strike."""
        return frame_index < len(self.rolls) and self.rolls[frame_index] == 10

    def _is_spare(self, frame_index):
        """Check if two rolls form a spare."""
        return (frame_index + 1 < len(self.rolls) and 
                self.rolls[frame_index] + self.rolls[frame_index + 1] == 10)

    def _strike_bonus(self, frame_index):
        """Bonus for a strike = next two rolls."""
        if frame_index + 2 < len(self.rolls):
            return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]
        elif frame_index + 1 < len(self.rolls):
            return self.rolls[frame_index + 1]
        else:
            return 0

    def _spare_bonus(self, frame_index):
        """Bonus for a spare = next roll."""
        if frame_index + 2 < len(self.rolls):
            return self.rolls[frame_index + 2]
        else:
            return 0
    
    def get_frame_scores(self):
        """
        Get individual frame scores for display purposes.
        
        Returns:
            list: List of scores for each frame (useful for debugging)
        """
        frame_scores = []
        frame_index = 0
        
        for frame in range(9):
            if self._is_strike(frame_index):
                frame_scores.append(10 + self._strike_bonus(frame_index))
                frame_index += 1
            elif self._is_spare(frame_index):
                frame_scores.append(10 + self._spare_bonus(frame_index))
                frame_index += 2
            else:
                if frame_index + 1 < len(self.rolls):
                    frame_scores.append(self.rolls[frame_index] + self.rolls[frame_index + 1])
                else:
                    frame_scores.append(self.rolls[frame_index] if frame_index < len(self.rolls) else 0)
                frame_index += 2
        
        frame_scores.append(self._score_tenth_frame(frame_index))
        return frame_scores

    def is_game_complete(self):
        """
        Check if the game is complete (all 10 frames finished).
        Handles open, spare, strike, and perfect game cases.
        """
        frame_index = 0
        for frame in range(9):
            if frame_index >= len(self.rolls):
                return False
            if self._is_strike(frame_index):
                frame_index += 1
            else:
                if frame_index + 1 >= len(self.rolls):
                    return False
                frame_index += 2

        # Tenth frame
        rolls_in_tenth = len(self.rolls) - frame_index
        if rolls_in_tenth < 2:
            return False

        if self._is_strike(frame_index) or self._is_spare(frame_index):
            return rolls_in_tenth >= 3
        else:
            return rolls_in_tenth >= 2
