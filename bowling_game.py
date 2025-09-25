


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
            
        Example:
            >>> game = BowlingGame()
            >>> game.roll(7)  # Knock down 7 pins
            >>> game.roll(2)  # Knock down 2 more pins
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
        
        Returns:
            int: Total score for the game (0-300)
            
        Example:
            >>> game = BowlingGame()
            >>> game.roll(10)  # Strike
            >>> game.roll(5)
            >>> game.roll(4) 
            >>> # ... more rolls
            >>> total = game.score()
        """
        score = 0
        frame_index = 0

     
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

       
        score += self._score_tenth_frame(frame_index)
        
        return score

    def _score_tenth_frame(self, frame_index):
        """
        Calculate score for the tenth frame with special rules.
        
        Tenth frame rules:
        - If strike: get 2 bonus rolls, score all 3 rolls
        - If spare: get 1 bonus roll, score all 3 rolls  
        - If open: score just the 2 rolls
        
        Args:
            frame_index (int): Starting index of the tenth frame
            
        Returns:
            int: Score for the tenth frame
        """
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
        """
        Check if the roll at frame_index is a strike.

        Args:
            frame_index (int): Index of the roll to check

        Returns:
            bool: True if the roll is a strike (10 pins), False otherwise
            
        Example:
            >>> game = BowlingGame()
            >>> game.roll(10)
            >>> game._is_strike(0)  # True
        """
        return frame_index < len(self.rolls) and self.rolls[frame_index] == 10

    def _is_spare(self, frame_index):
        """
        Check if the rolls at frame_index and frame_index + 1 form a spare.

        Args:
            frame_index (int): Index of the first roll in a frame

        Returns:
            bool: True if the two rolls total 10 pins, False otherwise
            
        Example:
            >>> game = BowlingGame()
            >>> game.roll(7)
            >>> game.roll(3)
            >>> game._is_spare(0)  # True
        """
        return (frame_index + 1 < len(self.rolls) and 
                self.rolls[frame_index] + self.rolls[frame_index + 1] == 10)

    def _strike_bonus(self, frame_index):
        """
        Calculate the bonus for a strike.

        Args:
            frame_index (int): Index of the strike roll

        Returns:
            int: The sum of the next two rolls after the strike
            
        Example:
            >>> game = BowlingGame()
            >>> game.roll(10)  # Strike
            >>> game.roll(5)   # Next roll
            >>> game.roll(3)   # Next roll  
            >>> bonus = game._strike_bonus(0)  # Returns 8
        """
        if frame_index + 2 < len(self.rolls):
            return self.rolls[frame_index + 1] + self.rolls[frame_index + 2]
        elif frame_index + 1 < len(self.rolls):
            return self.rolls[frame_index + 1]
        else:
            return 0

    def _spare_bonus(self, frame_index):
        """
        Calculate the bonus for a spare.

        Args:
            frame_index (int): Index of the first roll in a spare

        Returns:
            int: The value of the roll after the spare
            
        Example:
            >>> game = BowlingGame()
            >>> game.roll(7)   # First roll
            >>> game.roll(3)   # Spare completed
            >>> game.roll(5)   # Next roll
            >>> bonus = game._spare_bonus(0)  # Returns 5
        """
      
        if frame_index + 2 < len(self.rolls):
            return self.rolls[frame_index + 2]
        else:
            return 0
    
    def get_frame_scores(self):
        """
        Get individual frame scores for display purposes.
        
        Returns:
            list: List of scores for each frame (useful for debugging)
            
        Note:
            This is a helper method for testing and debugging.
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
        Check if the game is complete (all required rolls made).
        
        Returns:
            bool: True if game is complete, False otherwise
            
        Note:
            A complete game has:
            - 20 rolls for a game with no strikes/spares in 10th frame
            - 21 rolls for a spare in the 10th frame  
            - 22 rolls for a strike in the 10th frame
        """
        if len(self.rolls) < 18:
            return False
            
       
        rolls_needed = 20
        frame_index = 0
        
      
        for frame in range(9):
            if self._is_strike(frame_index):
                frame_index += 1
                rolls_needed -= 1
            else:
                frame_index += 2
        
      
        if frame_index < len(self.rolls):
            if self.rolls[frame_index] == 10:  
                rolls_needed += 2
            elif (frame_index + 1 < len(self.rolls) and 
                  self.rolls[frame_index] + self.rolls[frame_index + 1] == 10): 
                rolls_needed += 1
                
        return len(self.rolls) >= rolls_needed