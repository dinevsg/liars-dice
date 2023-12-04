<h1>Liars Dice</h1>
<p>
  Liar’s Dice is a social game of deception and strategy. Each player can only see the dice in their hand, but must make bids on ALL the dice, including ones hidden by their opponents. Players make bids and call bluffs on other players, while attempting to avoid losing challenges (and losing their dice!).
</p>
<h2>How to play</h2>
<p>Download all the files to your local system. Open them in your IDE and start "app.py" file.</p>
<h2>Rules</h2>
<h3>1. Play the first round by rolling all 5 dice and keeping them hidden</h3>
<p>
  To begin the first round, all players put all of their dice in their cup, shake it, and roll by flipping the cup over so their dice are hidden. They will peek underneath their cup to see what dice they have.
</p>
<h3>2. Place bet</h3>
<p>
  The first player begins the round by placing their bid. They will declare a quantity of dice (e.g. five) and the face value of the dice they’re bidding on (e.g. threes). With this bid, the player is saying that there are at least five dice between all players that are a three.
</p>
<h3>3. Play the next turn by increasing the bid or calling a "liar"</h3>
<p>
  Play continues and after each bid, the player is faced with 2 decisions:
  <ul>
    <li>Increase the bid</li>
      <p>Increasing bids on the next turn must be either: a higher face value and same quantity of dice (e.g. increasing from three fours to three fives or three sixes) OR a higher quantity of dice of any face value (e.g. increasing from three fours to four twos, etc).</p>
    <li>Call "Liar"</li>
      <p>When the turn rotates to a new player, if they believe that the bid exceeds the reality of what the dice reveal AND they feel so strongly that they’re willing to challenge, they can bluff by saying “liar”. Once "liar" is “called”, all players lift their cups to reveal their dice, and the quantity of the dice with bidded face value (plus the wild 1s) is counted. If the bidder doesn’t have enough of the dice called, they lose the round. If there are more dice of that face value than bid, the challenger who said "liar" loses the round. Whoever lost the round must remove one die from their cup, and they go first in the next round.</p>
  </ul>
</p>
<h3>4. Wild ones</h3>
  <p>You have the ability to activate wild ones mode.</br>1's are wild and can represent any face value in a bet. The exception is if the bet has a 1 as dice value in it. For example if a player bet two threes after revealing the dice all of the 1's in the game will be count as threes</p>
<h3>5. Game end</h3>
<p>The game ends whenever only one player is left with at least one die.</p>
<h2>The algorithm for bets and decisions</h2>
<p>
  Here is the tricky part</br>I managed to create an algorithm for CPU player's bet and CPU player's decision(bet or liar).
  <ul>
    <li>
      <p>For a proper bet by the CPU player I calculate that the player will never place a bet which will be impossible to win.
What does it mean? For example if there are 2 players in the game the total dice count will be 10(at some point). So if the player bets
ten fours but at least one die in their hand is not four (e.g. "4, 4, 4, 2") and in the best scenario the other player has "4, 4, 4, 4, 4," the maximum dice count of all the fours in the game will be 9. This is impossible-to-win bet so the CPU player will never bet anything like this</p>
    </li>
    <li>
      <p>Respectively almost the same algorithm is set for the player decision(bet or liar).
      Cpu player will subtract his total dice count and receive the total dice count for the other players. It makes sense when cpu player calculates that dice count bet from the previous player is impossible
      because cpu player does not have the needed quantity + the other dice count in total could not be equal or less than the previous player dice count bet. So the overall bet will not pass and the previous player is definitely a liar
      For example if there are 2 players in game, respectively there will be 10 dice (at some point) in the game.
      If previous player bet is '6: 2' in the best scenario the previous player has five dice with value '2'
      and cpu player does not have '2' in his hand (nor wild ones) cpu player immediately knows that this impossible-to-win bet, so his decision will be "liar".</p>
    </li>
  </ul>
</p>
<h2>Errors catching</h2>
<p>I am 99% sure that the game won't throw an error, whenever an invalid input is placed.
I tried to catch all of the possible errors the app could return, so I made an exceptions to them or just created a while loop preventing unwanted behavior.</p>
