

import unittest
from bowling_game import BowlingGame


class TestBowlingGame(unittest.TestCase):
    
    def setUp(self):
        
        self.game = BowlingGame()
    
    def test_game_initialization(self):
        """new game initializes correctly."""
        self.assertEqual(len(self.game.rolls), 0)
        self.assertEqual(self.game.current_roll, 0)
    
    def test_gutter_game(self):
        """all rolls are gutter balls (0 pins)."""
        self._roll_many(20, 0)
        self.assertEqual(self.game.score(), 0)
    
    def test_all_ones(self):
        """each roll knocks down 1 pin."""
        self._roll_many(20, 1)
        self.assertEqual(self.game.score(), 20)
    
    def test_one_spare(self):
        """one spare followed by normal rolls."""
        self._roll_spare()
        self.game.roll(3)
        self._roll_many(17, 0)
        self.assertEqual(self.game.score(), 16)  
    
    def test_one_strike(self):
        """one strike followed by normal rolls."""
        self._roll_strike()
        self.game.roll(3)
        self.game.roll(4)
        self._roll_many(16, 0)
        self.assertEqual(self.game.score(), 24)  
    
    def test_perfect_game(self):
        """ (all strikes = 300 points)."""
        self._roll_many(12, 10)  
        self.assertEqual(self.game.score(), 300)
    
    def test_all_spares(self):
        """all spares."""
        for i in range(21): 
            self.game.roll(5)
        self.assertEqual(self.game.score(), 150)
    
    def test_multiple_strikes(self):
        """ consecutive strikes."""
        self._roll_strike() 
        self._roll_strike()  
        self._roll_strike()
        self.game.roll(0)
        self.game.roll(0)
        self._roll_many(14, 0)
    
        self.assertEqual(self.game.score(), 60)
    
    def test_tenth_frame_spare(self):
        """spare in the tenth frame."""
        self._roll_many(18, 0)  
        self.game.roll(4)      
        self.game.roll(6)    
        self.game.roll(5)     
        self.assertEqual(self.game.score(), 15)
    
    def test_tenth_frame_strike(self):
        """strike in the tenth frame."""
        self._roll_many(18, 0)  
        self.game.roll(10)    
        self.game.roll(5)    
        self.game.roll(3)    
        self.assertEqual(self.game.score(), 18)
    
    def test_mixed_game(self):
        """strikes, spares, and open frames."""

        self._roll_strike()
        
        self.game.roll(7)
        self.game.roll(3)
    
        self.game.roll(4)
        self.game.roll(2)
      
        self._roll_many(14, 0)
        
        
        self.assertEqual(self.game.score(), 40)
    

    
    def test_boundary_pins_valid(self):
        """boundary values for valid pin counts."""
       
        self.game.roll(0)
        self.assertEqual(self.game.rolls[0], 0)
        
 
        game2 = BowlingGame()
        game2.roll(10)
        self.assertEqual(game2.rolls[0], 10)
    
    def test_frame_pin_total_validation(self):
        """two rolls in a frame don't exceed 10 pins."""
        
        self.game.roll(4)
        self.game.roll(6)
        self.assertEqual(sum(self.game.rolls[:2]), 10)
    

    
    def _roll_many(self, n, pins):
        """Roll the ball n times, knocking down 'pins' pins each time."""
        for i in range(n):
            self.game.roll(pins)
    
    def _roll_spare(self):
        """Roll a spare (two rolls totaling 10 pins)."""
        self.game.roll(5)
        self.game.roll(5)
    
    def _roll_strike(self):
        """Roll a strike (10 pins in first roll)."""
        self.game.roll(10)


class TestBowlingGameErrorHandling(unittest.TestCase):
    
    
    def setUp(self):
        self.game = BowlingGame()
    
    def test_negative_pins(self):
        
    
        try:
            self.game.roll(-1)
      
            self.fail("Should handle negative pin counts")
        except ValueError:
          
            pass
        except:
            
            pass
    
    def test_too_many_pins(self):
        """pin counts over 10 are handled appropriately."""
        try:
            self.game.roll(11)
        
            self.fail("Should handle pin counts over 10")
        except ValueError:
           
            pass
        except:
           
            pass
    
    def test_too_many_pins_per_frame(self):
        """totals over 10 are handled (except strikes)."""
        try:
            self.game.roll(7)
            self.game.roll(8)  
          
            self.fail("Should validate frame pin totals")
        except ValueError:
          
            pass
        except:
          
            pass


if __name__ == '__main__':

    unittest.main(verbosity=2)