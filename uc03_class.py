import math
import operator

def normalizer(vals):
	avg = sum(vals) / len(vals)
	sq_sum = 0
	for i in vals:
		sq_sum += pow(i - avg, 2)
	dev = pow(sq_sum/len(vals), 0.5)
	norm_vals = []
	for i in vals:
		norm_i = round((i - avg) /dev, 3)
		norm_vals.append(norm_i)
	return norm_vals

def rcusage_scoring(rcusage,weight=1):
	#rcusage += 1
	#pct = rcusage/12.0
	pct = rcusage/11.0
	factor_score = pct*weight
	rc_score = 1 - pow(0.8, factor_score)
	return rc_score
	
def profit_share_scoring(profit_share):
	if profit_share == 0:
		profit_share = global_profit_share_zero_value
	factor_score = profit_share*global_profit_share_weight
	profit_share_score = 1 - pow(global_profit_share_base, factor_score)
	return profit_share_score
	
def base_scoring(profit_share,rcusage,):
	rc_score = rcusage_scoring(rcusage)
	#ps_score = profit_share_scoring(profit_share)
	ps_score = profit_share_scoring(profit_share)
	score = (rc_score + ps_score) / 5
	return(score)
	
def folio_scoring(gen=0, spec=0, spec_weight=3, gen_weight=1,multiplier=0.05):
    ## want to return the number of specific page views that are required for a 0/0 article to overcome the top-scoring article
    ## should iterate over possible number of general pages
    spec_exp = multiplier * (gen_weight * gen + spec_weight * spec)
    score_spec = 1 - pow(0.4, spec_exp)
    return score_spec
	
def web_scoring(gen=0, spec=0, spec_weight=3, gen_weight=1,multiplier=0.05):
    ## want to return the number of specific page views that are required for a 0/0 article to overcome the top-scoring article
    ## should iterate over possible number of general pages
    spec_exp = multiplier * (gen_weight * gen + spec_weight * spec)
    score_spec = 1 - pow(0.2, spec_exp)
    return score_spec
	
def email_scoring(gen=0, spec=0, spec_weight=3, gen_weight=1,multiplier=0.05):
    ## want to return the number of specific page views that are required for a 0/0 article to overcome the top-scoring article
    ## should iterate over possible number of general pages
    spec_exp = multiplier * (gen_weight * gen + spec_weight * spec)
    score_spec = 1 - pow(0.6, spec_exp)
    return score_spec	
	
def calc_score(base_score, web_gen = 0, web_gen_weight = 3, web_spec = 0, web_spec_weight = 1, folio_gen = 0, folio_gen_weight = 1, folio_spec = 0, folio_spec_weight = 3, email_gen = 0, email_gen_weight = 1, email_spec = 0, email_spec_weight = 3, web_multiplier = 0.05, email_multiplier = 0.05, folio_multiplier = 0.05):
	web_score = web_scoring(web_gen, web_spec,web_spec_weight,web_gen_weight,web_multiplier)
	folio_score = folio_scoring(folio_gen, folio_spec,folio_spec_weight,folio_gen_weight,folio_multiplier)
	email_score = email_scoring(email_gen, email_spec,email_spec_weight,email_gen_weight,email_multiplier)
	fixed_score = base_scoring
	score = 0.2 * (web_score + email_score + folio_score) + base_score
	return score

def reweigh_profit_share(base=0.1, zero=0, weight=0.5):
	global global_profit_share_base
	global global_profit_share_zero_value
	global global_profit_share_weight
	global_profit_share_base = base
	global_profit_share_zero_value = zero
	global_profit_share_weight = weight
	
## variables for all articles:
global_web_gen_weight = 1
global_web_spec_weight = 3
global_web_multiplier = 0.05
global_folio_gen_weight = 1
global_folio_spec_weight = 3
global_folio_multiplier = 0.05
global_email_gen_weight = 1
global_email_spec_weight = 3
global_email_multiplier = 0.05
global_profit_share_base = 0.1
global_profit_share_zero_value = 0
global_profit_share_weight = 0.5

class Scorer:
	def scoring(self):
		self.web_score = web_scoring(self.web_gen, self.web_spec, global_web_spec_weight, global_web_gen_weight, self.web_multiplier)
		self.folio_score = folio_scoring(self.folio_gen, self.folio_spec, global_folio_spec_weight, global_folio_gen_weight, self.folio_multiplier)
		self.email_score = email_scoring(self.email_gen, self.email_spec, global_email_spec_weight, global_email_gen_weight, self.email_multiplier)
		self.base_score = base_scoring(self.spec_profit, self.spec_rc)
		#self.score = calc_score(self.base_score, self.web_gen,global_web_gen_weight,self.web_spec,global_web_spec_weight,self.folio_gen,global_folio_gen_weight,self.folio_spec,global_folio_spec_weight,self.email_gen,global_email_gen_weight,self.email_spec,global_email_spec_weight,global_web_multiplier,global_email_multiplier,global_folio_multiplier)
		self.score = calc_score(self.base_score, self.web_gen,global_web_gen_weight,self.web_spec,global_web_spec_weight,self.folio_gen,global_folio_gen_weight,self.folio_spec,global_folio_spec_weight,self.email_gen,global_email_gen_weight,self.email_spec,global_email_spec_weight,self.web_multiplier,self.email_multiplier,self.folio_multiplier)
		
	def __init__(self, spec_profit, spec_rc, gen_rc = 11, gen_profit = 0.75, web_gen = 0, web_gen_weight = 1, web_spec = 0, web_spec_weight = 3, folio_gen = 0, folio_gen_weight = 1, folio_spec = 0, folio_spec_weight = 3, email_gen = 0, email_gen_weight = 1, email_spec = 0, email_spec_weight = 3, web_multiplier = 0.05, email_multiplier = 0.05, folio_multiplier = 0.05):
		self.spec_rc = spec_rc
		self.spec_profit = spec_profit
		self.gen_rc = gen_rc
		self.gen_profit = gen_profit
		self.web_gen = web_gen
		#self.web_gen_weight = web_gen_weight
		self.web_spec = web_spec
		self.web_spec_weight = web_spec_weight
		self.folio_gen = folio_gen
		self.folio_gen_weight = folio_gen_weight
		self.folio_spec = folio_spec
		self.folio_spec_weight = folio_spec_weight
		self.email_gen = email_gen
		self.email_gen_weight = email_gen_weight
		self.email_spec = email_spec
		self.email_spec_weight = email_spec_weight
		self.web_multiplier = web_multiplier
		self.email_multiplier = email_multiplier
		self.folio_multiplier = folio_multiplier
		
		self.base_score = base_scoring(self.spec_profit, self.spec_rc)
		self.scoring()
		
	def recalc_base_scoring(self):
		self.base_score = base_scoring(self.spec_profit, self.spec_rc)
		#self.base_score = base_scoring(self.spec_profit, self.spec_rc,profit_share_base, profit_share_zero_value)
		
	def compare(self, obj):
		self.scoring()
		obj.scoring()
		if self.score > obj.score:
			print("bigger")
		else:
			print("smaller")
			
	def web_scoring_test(self, gen, spec):
		old_web_spec_1 = self.web_spec	
		old_web_gen_1 = self.web_gen
		
		self.web_spec = spec
		self.web_gen = gen
		self.scoring()
		return self.score
		
		self.web_spec	= old_web_spec_1 
		self.web_gen = old_web_gen_1
		self.scoring()
		
	def compare_iter(self, obj, folio_flag=0):	
		old_web_spec_1 = self.web_spec	
		old_web_gen_1 = self.web_gen
		old_web_spec_2 = obj.web_spec	
		old_web_gen_2 = obj.web_gen
		
		self.web_spec = 0	
		obj.web_spec = 0	
			
		for i in range (0,11):
			for j in range(1,11):
				self.web_spec = j
				self.web_gen = i
				obj.web_gen = i + j
				self.scoring()
				obj.scoring()
				if self.score > obj.score:
					print("spec wins with " + str(i) + " general page views and " + str(j) + " specific page views")
					print("general score: " + str(obj.score))
					print("specific score: " + str(self.score))
					break
				elif (obj.score - self.score) < 0.2 and folio_flag:
					for x in range (0,11):
						for y in range (1,6):
							self.folio_spec = y
							self.folio_gen = x
							obj.folio_gen = x + y
							self.scoring()
							obj.scoring()
							if self.score > obj.score:
								print("spec wins with " + str(i) + " general page views and " + str(j) + " specific page views and " + str(x) + " general folio buys and " + str(y) +" specific folio buys")
								print("general score: " + str(obj.score))
								print("specific score: " + str(self.score))
								break
							self.folio_spec = 0
							self.folio_gen = 0
							obj.folio_gen = 0
					
		## could also do folio, click data only if score is within < 0.4, max score for the two other factors			
					
					
		self.web_spec	= old_web_spec_1 
		self.web_gen = old_web_gen_1
		obj.web_spec = old_web_spec_2
		obj.web_gen = old_web_gen_2
		self.scoring()
		obj.scoring()
			
			
### some values:			
bouchon = Scorer(0.5, 0)
bouchon.scoring()
buddy_v = Scorer(0.75,0)			
buddy_v.scoring()
cut = Scorer(0.75, 11)
cut.scoring()
delmonico = Scorer(0,10)
delmonico.scoring()
tao = Scorer(0,0)	
tao.scoring()

## cut, delmonico compare: old
def re_weigh_c_d(web_gen_weight, web_spec_weight, web_multiplier):
	cut.web_gen_weight = web_gen_weight
	cut.web_spec_weight = web_spec_weight
	cut.web_multiplier = web_multiplier
	delmonico.web_gen_weight = web_gen_weight
	delmonico.web_spec_weight = web_spec_weight
	delmonico.web_multiplier = web_multiplier
	
	cut.scoring()
	delmonico.scoring()

def page_visit_c_d(c, d, other):
	cut.web_spec = c
	delmonico.web_spec = d
	cut.web_gen = d + other
	delmonico.web_gen = c + other
	
	cut.scoring()
	delmonico.scoring()

	print("cut score " + str(cut.score))
	print("delmonico score " + str(delmonico.score))

######## all values:
bellini= Scorer(1,0)
black = Scorer(0.75,0)
bouchon= Scorer(0.50,0)
baz= Scorer(1,0)
human= Scorer(0,0)
buddy= Scorer(0.75,0)
canyon= Scorer(0,0)
chica= Scorer(0,0)
cut= Scorer(0.75,11)
delmonico= Scorer(0,10)
gondola = Scorer(1,0)
grand_lux = Scorer(0,1)
hong_kong = Scorer(1,0)
isd= Scorer(1,2)
lagasse= Scorer(0.93,0)
lavo= Scorer(0,0)
morel= Scorer(0,0)
noodle_asia= Scorer(0,8)
pools = Scorer(1,4)
public_house= Scorer(0,0)
race= Scorer(1,0)
rosina = Scorer(1,0)
solaro= Scorer(1,0)
sugarcane = Scorer(0,0)
sushisamba= Scorer(0,9)
tao= Scorer(0,0)
aquatic= Scorer(1,0)
dorsey= Scorer(1,7)
yardbird = Scorer(0.75,0)

# adjustments:
baz.web_multiplier = 0.087
baz.folio_multiplier = 0.148
human.web_multiplier = 0.087
human.folio_multiplier = 0.148
baz.scoring()
human.scoring()

canyon.web_multiplier = 0.065
canyon.folio_multiplier = 0.086
gondola.web_multiplier = 0.065
gondola.folio_multiplier = 0.086
isd.web_multiplier = 0.065
isd.folio_multiplier = 0.086
pools.web_multiplier = 0.065
pools.folio_multiplier = 0.086
aquatic.web_multiplier = 0.065
aquatic.folio_multiplier = 0.086
canyon.scoring()
gondola.scoring()
isd.scoring()
pools.scoring()
aquatic.scoring()

race.web_multiplier = 0.061
race.web_multiplier = 0.119
race.scoring()

def recalc_all_score():
	 bellini.scoring()
	 black.scoring()
	 bouchon.scoring()
	 baz.scoring()
	 human.scoring()
	 buddy.scoring()
	 canyon.scoring()
	 chica.scoring()
	 cut.scoring()
	 delmonico.scoring()
	 gondola.scoring()
	 grand_lux.scoring()
	 hong_kong.scoring()
	 isd.scoring()
	 lagasse.scoring()
	 lavo.scoring()
	 morel.scoring()
	 noodle_asia.scoring()
	 pools .scoring()
	 public_house.scoring()
	 race.scoring()
	 rosina .scoring()
	 solaro.scoring()
	 sugarcane .scoring()
	 sushisamba.scoring()
	 tao.scoring()
	 aquatic.scoring()
	 dorsey.scoring()
	 yardbird.scoring()
	 
def get_all_scores():
	scores = {}
	scores["bellini"] = bellini.score
	scores["black"] = black.score
	scores["bouchon"] = bouchon.score
	scores["baz"] = baz.score
	scores["human"] = human.score
	scores["buddy"] = buddy.score
	scores["canyon"] = canyon.score
	scores["chica"] = chica.score
	scores["cut"] = cut.score
	scores["delmonico"] = delmonico.score
	scores["gondola"] = gondola.score
	scores["grand_lux"] = grand_lux.score
	scores["hong_kong"] = hong_kong.score
	scores["isd"] = isd.score
	scores["lagasse"] = lagasse.score
	scores["lavo"] = lavo.score
	scores["morel"] = morel.score
	scores["noodle_asia"] = noodle_asia.score
	scores["pools"] = pools .score
	scores["public_house"] = public_house.score
	scores["race"] = race.score
	scores["rosina"] = rosina .score
	scores["solaro"] = solaro.score
	scores["sugarcane"] = sugarcane .score
	scores["sushisamba"] = sushisamba.score
	scores["tao"] = tao.score
	scores["aquatic"] = aquatic.score
	scores["dorsey"] = dorsey.score
	scores["yardbird"] = yardbird.score
	sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=1)
	for (i,j) in sorted_scores:
		print(i + ": " + str(j))
	
def inc_restaurant_web(restaurant=None, num=1):
	bellini.web_gen += num
	black.web_gen += num
	bouchon.web_gen += num
	buddy.web_gen += num
	chica.web_gen += num
	cut.web_gen += num
	delmonico.web_gen += num
	grand_lux.web_gen += num
	hong_kong.web_gen += num
	lagasse.web_gen += num
	lavo.web_gen += num
	morel.web_gen += num
	noodle_asia.web_gen += num
	public_house.web_gen += num
	rosina .web_gen += num
	solaro.web_gen += num
	sugarcane .web_gen += num
	sushisamba.web_gen += num
	tao.web_gen += num
	dorsey.web_gen += num
	yardbird.web_gen += num
	if restaurant != None:
		restaurant.web_gen -= num
		restaurant.web_spec += num
	recalc_all_score()
	
def inc_restaurant_folio(restaurant=None, num=1):
	bellini.folio_gen += num
	black.folio_gen += num
	bouchon.folio_gen += num
	buddy.folio_gen += num
	chica.folio_gen += num
	cut.folio_gen += num
	delmonico.folio_gen += num
	grand_lux.folio_gen += num
	hong_kong.folio_gen += num
	lagasse.folio_gen += num
	lavo.folio_gen += num
	morel.folio_gen += num
	noodle_asia.folio_gen += num
	public_house.folio_gen += num
	rosina .folio_gen += num
	solaro.folio_gen += num
	sugarcane .folio_gen += num
	sushisamba.folio_gen += num
	tao.folio_gen += num
	dorsey.folio_gen += num
	yardbird.folio_gen += num
	if restaurant != None:
		restaurant.folio_gen -= num
		restaurant.folio_spec += num
	recalc_all_score()
	
def reset_web():
	bellini.web_gen = 0
	black.web_gen = 0 
	black.web_spec = 0
	bouchon.web_gen = 0 
	bouchon.web_spec = 0
	buddy.web_gen = 0 
	buddy.web_spec = 0
	chica.web_gen = 0 
	chica.web_spec = 0
	cut.web_gen = 0 
	cut.web_spec = 0
	delmonico.web_gen = 0 
	delmonico.web_spec = 0
	grand_lux.web_gen = 0 
	grand_lux.web_spec = 0
	hong_kong.web_gen = 0 
	hong_kong.web_spec = 0
	lagasse.web_gen = 0 
	lagasse.web_spec = 0
	lavo.web_gen = 0 
	lavo.web_spec = 0
	morel.web_gen = 0 
	morel.web_spec = 0
	noodle_asia.web_gen = 0 
	noodle_asia.web_spec = 0
	public_house.web_gen = 0 
	public_house.web_spec = 0
	rosina.web_gen = 0
	rosina.web_spec = 0
	solaro.web_gen = 0 
	solaro.web_spec = 0
	sugarcane.web_gen = 0
	sugarcane.web_spec = 0
	sushisamba.web_gen = 0 
	sushisamba.web_spec = 0
	tao.web_gen = 0 
	tao.web_spec = 0
	dorsey.web_gen = 0 
	dorsey.web_spec = 0
	yardbird.web_gen = 0 
	yardbird.web_spec = 0
	baz.web_gen = 0
	baz.web_spec = 0
	human.web_gen = 0
	human.web_spec = 0
	bellini.web_gen = 0 
	bellini.web_spec = 0
	canyon.web_gen = 0 
	canyon.web_spec = 0
	gondola.web_gen = 0 
	gondola.web_spec = 0
	isd.web_gen = 0 
	isd.web_spec = 0
	pools.web_gen = 0 
	pools.web_spec = 0
	aquatic.web_gen = 0 
	aquatic.web_spec = 0
	recalc_all_score()		
	
def reset_email():
	bellini.email_gen = 0
	black.email_gen = 0 
	black.email_spec = 0
	bouchon.email_gen = 0 
	bouchon.email_spec = 0
	buddy.email_gen = 0 
	buddy.email_spec = 0
	chica.email_gen = 0 
	chica.email_spec = 0
	cut.email_gen = 0 
	cut.email_spec = 0
	delmonico.email_gen = 0 
	delmonico.email_spec = 0
	grand_lux.email_gen = 0 
	grand_lux.email_spec = 0
	hong_kong.email_gen = 0 
	hong_kong.email_spec = 0
	lagasse.email_gen = 0 
	lagasse.email_spec = 0
	lavo.email_gen = 0 
	lavo.email_spec = 0
	morel.email_gen = 0 
	morel.email_spec = 0
	noodle_asia.email_gen = 0 
	noodle_asia.email_spec = 0
	public_house.email_gen = 0 
	public_house.email_spec = 0
	rosina.email_gen = 0
	rosina.email_spec = 0
	solaro.email_gen = 0 
	solaro.email_spec = 0
	sugarcane.email_gen = 0
	sugarcane.email_spec = 0
	sushisamba.email_gen = 0 
	sushisamba.email_spec = 0
	tao.email_gen = 0 
	tao.email_spec = 0
	dorsey.email_gen = 0 
	dorsey.email_spec = 0
	yardbird.email_gen = 0 
	yardbird.email_spec = 0
	baz.email_gen = 0
	baz.email_spec = 0
	human.email_gen = 0
	human.email_spec = 0
	bellini.email_gen = 0 
	bellini.email_spec = 0
	canyon.email_gen = 0 
	canyon.email_spec = 0
	gondola.email_gen = 0 
	gondola.email_spec = 0
	isd.email_gen = 0 
	isd.email_spec = 0
	pools.email_gen = 0 
	pools.email_spec = 0
	aquatic.email_gen = 0 
	aquatic.email_spec = 0
	recalc_all_score()	

def reset_folio():
	bellini.folio_gen = 0
	black.folio_gen = 0 
	black.folio_spec = 0
	bouchon.folio_gen = 0 
	bouchon.folio_spec = 0
	buddy.folio_gen = 0 
	buddy.folio_spec = 0
	chica.folio_gen = 0 
	chica.folio_spec = 0
	cut.folio_gen = 0 
	cut.folio_spec = 0
	delmonico.folio_gen = 0 
	delmonico.folio_spec = 0
	grand_lux.folio_gen = 0 
	grand_lux.folio_spec = 0
	hong_kong.folio_gen = 0 
	hong_kong.folio_spec = 0
	lagasse.folio_gen = 0 
	lagasse.folio_spec = 0
	lavo.folio_gen = 0 
	lavo.folio_spec = 0
	morel.folio_gen = 0 
	morel.folio_spec = 0
	noodle_asia.folio_gen = 0 
	noodle_asia.folio_spec = 0
	public_house.folio_gen = 0 
	public_house.folio_spec = 0
	rosina.folio_gen = 0
	rosina.folio_spec = 0
	solaro.folio_gen = 0 
	solaro.folio_spec = 0
	sugarcane.folio_gen = 0
	sugarcane.folio_spec = 0
	sushisamba.folio_gen = 0 
	sushisamba.folio_spec = 0
	tao.folio_gen = 0 
	tao.folio_spec = 0
	dorsey.folio_gen = 0 
	dorsey.folio_spec = 0
	yardbird.folio_gen = 0 
	yardbird.folio_spec = 0
	baz.folio_gen = 0
	baz.folio_spec = 0
	human.folio_gen = 0
	human.folio_spec = 0
	bellini.folio_gen = 0 
	bellini.folio_spec = 0
	canyon.folio_gen = 0 
	canyon.folio_spec = 0
	gondola.folio_gen = 0 
	gondola.folio_spec = 0
	isd.folio_gen = 0 
	isd.folio_spec = 0
	pools.folio_gen = 0 
	pools.folio_spec = 0
	aquatic.folio_gen = 0 
	aquatic.folio_spec = 0
	recalc_all_score()	

def inc_restaurant_email(restaurant=None, num=1):
	bellini.email_gen += num
	black.email_gen += num
	bouchon.email_gen += num
	buddy.email_gen += num
	chica.email_gen += num
	cut.email_gen += num
	delmonico.email_gen += num
	grand_lux.email_gen += num
	hong_kong.email_gen += num
	lagasse.email_gen += num
	lavo.email_gen += num
	morel.email_gen += num
	noodle_asia.email_gen += num
	public_house.email_gen += num
	rosina .email_gen += num
	solaro.email_gen += num
	sugarcane .email_gen += num
	sushisamba.email_gen += num
	tao.email_gen += num
	dorsey.email_gen += num
	yardbird.email_gen += num
	if restaurant != None:
		restaurant.email_gen -= num
		restaurant.email_spec += num	
	recalc_all_score()	

def inc_entertainment_email(entertainment=None, num=1):
	baz.email_gen += num
	human.email_gen += num
	if entertainment != None:
		entertainment.email_gen -= num
		entertainment.email_spec += num
	recalc_all_score()
	
def inc_entertainment_folio(entertainment=None, num=1):
	baz.folio_gen += num
	human.folio_gen += num
	if entertainment != None:
		entertainment.folio_gen -= num
		entertainment.folio_spec += num
	recalc_all_score()

def inc_entertainment_web(entertainment=None, num=1):
	baz.web_gen += num
	human.web_gen += num
	if entertainment != None:
		entertainment.web_gen -= num
		entertainment.web_spec += num
	recalc_all_score()
	
def inc_resort_web(resort=None, num=1):
	bellini.web_gen += num
	canyon.web_gen += num
	gondola.web_gen += num
	isd.web_gen += num
	pools.web_gen += num
	aquatic.web_gen += num
	if resort != None:
		resort.web_gen -= num
		resort.web_spec += num
	recalc_all_score()
	
def inc_resort_folio(resort=None, num=1):
	bellini.folio_gen += num
	canyon.folio_gen += num
	gondola.folio_gen += num
	isd.folio_gen += num
	pools.folio_gen += num
	aquatic.folio_gen += num
	if resort != None:
		resort.folio_gen -= num
		resort.folio_spec += num
	recalc_all_score()
	
def inc_resort_folio(resort=None, num=1):
	bellini.folio_gen += num
	canyon.folio_gen += num
	gondola.folio_gen += num
	isd.folio_gen += num
	pools.folio_gen += num
	aquatic.folio_gen += num
	if resort != None:
		resort.folio_gen -= num
		resort.folio_spec += num
	recalc_all_score()

def set_conf_default():
	global global_web_gen_weight
	global_web_gen_weight = 1
	reweigh_profit_share()
	recalc_all_score()
	
def	set_conf_1():
	global global_web_gen_weight
	global_web_gen_weight = 0.3
	
	## base, zero value
	reweigh_profit_share(0.5, 0.1)

	recalc_all_score()
	
def	set_conf_2():
	global global_web_gen_weight
	global_web_gen_weight = 0.3
	
	## base, zero value
	reweigh_profit_share(0.5)

	recalc_all_score()
	
def	set_conf_3():
	global global_web_gen_weight
	global_web_gen_weight = 0.3
	
	## base, zero value
	reweigh_profit_share(0.1, 0, 0.2)

	recalc_all_score()	
	
def	set_conf_4():
	global global_web_gen_weight
	global_web_gen_weight = 0.5
	
	## base, zero value
	reweigh_profit_share(0.1, 0, 0.2)

	recalc_all_score()		
###
# test 
