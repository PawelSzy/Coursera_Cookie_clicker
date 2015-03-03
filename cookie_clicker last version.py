"""
Cookie Clicker Simulator
"""

import simpleplot


# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
NAME = 0
COST = 1
CPS = 2

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        
        #The current number of cookies you have
        self._number_cookies = 0.0 
        #the total number of cookies produced throughout the entire game
        self._entire_game_cookies = 0.0
       
        self._cps = 1.0
        self._time = 0.0
        
        self._clicker_history = [(0.0, None, 0.0, 0.0)]

        
    def __str__(self):
        """
        Return human readable state
        """
        return_str = ""
        return_str+="\nnr cookies: "+ str(self.get_cookies())
        return_str+=", cps: "+str(self.get_cps())
        return_str+=", time: "+str(self.get_time())
        #return_str+="\nhistory:\n" +str(self.get_history())
        return return_str
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return  self._number_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._clicker_history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if self.get_cookies() >=cookies:
            return 0
        else:
            
            
            time = (cookies-self.get_cookies())/self._cps 
            if time < 0:
                return 0
            
            if time <1:
                return 1
            if time - round(time,0) <1:
                return round(time,0)+1
            return round(time,0)
        
        
        return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time <= 0:
            return None
        
        self._time+=time
        
        new_cookies = time*self._cps
        self._number_cookies+=time*self._cps
        self._entire_game_cookies+=new_cookies
        
        
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost > self.get_cookies():
            return None
        
        
        self._number_cookies-=cost
        self._cps+=additional_cps
        
        new_history_item = (self.get_time(), item_name, cost,self._entire_game_cookies)
        self._clicker_history.append(new_history_item)
        
        return new_history_item 
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    #clone build_info
    b_info = build_info.clone()
    
    clicker = ClickerState()
    #print "---------build info-------"
    #print duration
    #print b_info.build_items()
    #print "-----------"
    
    
    
    #main loo
    while True:    
        item = strategy(clicker.get_cookies(), clicker.get_cps(), clicker.get_time(), b_info)
        if item == None:
            break
        #print clicker
        #print "item: ", item
        cost = b_info.get_cost(item)
        #print "cost", cost
        #print "clicker.time_until(cost): ", clicker.time_until(cost)
        
        #jeœli zostanie przekroczony czas, przerwij
        time_until = clicker.time_until(cost)
        if clicker.get_time() +time_until > duration:
            break
        
        clicker.wait(time_until)
        
        #buy item
        cps_item = b_info.get_cps(item)
        while clicker.buy_item(item, cost, cps_item)!=None:
            b_info.update_item(item)
        #print clicker
        #print clicker.get_history()
    
    print "\nclicker:", clicker
    print clicker.get_history()
    print "--------end_build_info-------"    
    # Replace with your code
    return ClickerState()


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Return the cheapest item 
    """
    try:
        items = build_info.build_items()
    except Exception:
        return None    
    best_item = items[0]
    for item in items:
        try:
            if build_info.get_cost(item) < build_info.get_cost(best_item):
                best_item = item
        except Exception:
            return None
     
    if build_info.get_cost(best_item) >cookies + cps*time_left:
        return None
        
    return best_item

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Return the most expensive item 
    """
    
    items = build_info.build_items()
    best_item = items[0]
    for item in items:
        if build_info.get_cost(item) > build_info.get_cost(best_item):
            best_item = item
    
    if build_info.get_cost(best_item) >cookies + cps*time_left:
        return None
    
    return best_item

def strategy_best(cookies, cps, time_left, build_info):
    """
    Optymal strategy for winning - strategy best
    """
    #print "best"
    items = build_info.build_items()
    items_par = [(item, build_info.get_cost(item), build_info.get_cps(item)) for item in items]

    #constant - use names not field number
    #NAME = 0
    #COST = 1
    #CPS = 2
    
    #ratio - lambda function - oblicza stosunek CPS do kosztu
    ratio = lambda item: item[CPS]/item[COST]
    
    
    # chose best ration 
    best_ratio = (items_par[0][NAME], ratio(items_par[0]))
    
    for item in items_par:
        if best_ratio[1] < ratio(item):
            best_ratio = item
    #print "b_ration:", best_ratio
    return best_ratio[NAME]
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
    clicker = ClickerState

import poc_simpletest

def run_test(ClickerState):
    """
    Some informal testing code
    """
    
    print"-------------"
    print "start testing"
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    # create a game
    clicker = ClickerState()
    
    
    str_initial="\nnr cookies: 0.0, cps: 1.0, time: 0.0"
    
    # test the initial configuration of the board using the str method
    suite.run_test(str(clicker), str_initial, "Test #0: init")
    
    history =[(0.0, None, 0.0, 0.0)]
    #test the initial history
    suite.run_test(clicker.get_history(), history, "Test #1: history")
    
    #test the wait
    clicker.wait(10)
    expected_str = "\nnr cookies: 10.0, cps: 1.0, time: 10.0"
    suite.run_test(str(clicker), expected_str, "Test #2: wait")
    
    
    #test time until 
    suite.run_test(clicker.time_until(40), 30, "Test #3: time until")
    
    #test buy item
    #test buy item you don't have money
    suite.run_test(clicker.buy_item("sluzba", 300, 200), None, "Test #4 buy, too much")
                   
    #test buy item you have money
    suite.run_test(clicker.buy_item("gremliny", 5, 20), (10.0, 'gremliny', 5, 10.0), "Test #4 buy, too much")
    
    



def build_info_test(build_info):
    """
    Testing build_info
    """
    print "build_info_test"
    
    suite = poc_simpletest.TestSuite()
    items = build_info.build_items()
    for item in items:
        print item, build_info.get_cost(item)
    try:    
        suite.run_test(build_info.get_cost("Nie ma"), None, "Test b_info#1: item not in build info")    
    except KeyError:
        return "KeyError"

print "test"    
run_test(ClickerState)

#run()


print build_info_test(provided.BuildInfo())


#run()

#run_strategy("Expensive", SIM_TIME, strategy_expensive)
run_strategy("Cheap", SIM_TIME, strategy_cheap)
run_strategy("Best", SIM_TIME, strategy_best)
v