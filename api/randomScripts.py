#from models import ItemType,Supplier,OnSaleItem
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from decimal import Decimal
import requests
import re
from datetime import datetime,timedelta
def main():
    print "this is random scripts"
    webscrapMyGroceryDeals()

def webscrapMyGroceryDeals():
    print "webscrapping time"
    items_map = {'asparagus':638,'broccoli':639,'carrots':640,'cauliflower':641,'celery':642,'corn':643,'cucumbers':644,'lettuce':645,'mushrooms':646,'onions':647,'peppers':648,'potatoes':649,'spinach':650,'squash':651,'zucchini':652,'tomatoes':653,'apples':654,'avocados':655,'bananas':656,'berries':657,'cherries':658,'grapefruit':659,'grapes':660,'kiwis':661,'lemons':662,'limes':663,'melon':664,'nectarines':665,'oranges':666,'peaches':667,'pears':668,'plums':669,'chip_dip':670,'eggs':671,'fake_eggs':672,'english_muffins':673,'fruit_juice':674,'hummus':675,'ready-bake_breads':676,'tofu':677,'tortillas':678,'frozen_breakfasts':679,'frozen_burritos':680,'fish_sticks':681,'fries':682,'tater_tots':683,'ice_cream':684,'sorbet':685,'juice_concentrate':686,'pizza':687,'pizza_rolls':688,'popsicles':689,'tv_dinners':690,'vegetables':691,'bbq_sauce':692,'gravy':693,'honey':694,'hot_sauce':695,'jelly':696,'jam':697,'preserves':698,'ketchup':699,'mustard':700,'mayonnaise':701,'pasta_sauce':702,'relish':703,'salad_dressing':704,'salsa':705,'soy_sauce':706,'steak_sauce':707,'syrup':708,'worcestershire_sauce':709,'bouillon_cubes':710,'cereal':711,'coffee':712,'coffee_filters':713,'instant_potatoes':714,'lemon_juice':715,'lime_juice':716,'mac_&_cheese':717,'olive_oil':718,'packaged_meals':719,'pancake_mix':720,'waffle_mix':721,'pasta':722,'peanut_butter':723,'pickles':724,'rice':725,'tea':726,'vegetable_oil':727,'vinegar':728,'applesauce':729,'baked_beans':730,'broth':731,'canned_fruit':732,'canned_olives':733,'tinned_meats':734,'canned_tuna':735,'canned_chicken':736,'canned_soup':737,'chili':738,'canned_tomatoes':739,'canned_veggies':740,'basil':741,'black_pepper':742,'cilantro':743,'cinnamon':744,'garlic':745,'ginger':746,'mint':747,'oregano':748,'paprika':749,'parsley':750,'red_pepper':751,'salt':752,'vanilla_extract':753,'butter':754,'margarine':755,'half_&_half':756,'milk':757,'sour_cream':758,'whipped_cream':759,'yogurt':760,'bleu_cheese':761,'cheddar':762,'cottage_cheese':763,'cream_cheese':764,'feta':765,'goat_cheese':766,'mozzarella':767,'parmesan':768,'provolone':769,'ricotta':770,'sandwich_slices':771,'swiss':772,'bacon':773,'sausage':774,'beef':775,'steak':776,'chicken':777,'ground_beef':778,'turkey':779,'ham':780,'pork':781,'hot_dogs':782,'lunchmeat':783,'catfish':784,'crab':785,'lobster':786,'mussels':787,'oysters':788,'salmon':789,'shrimp':790,'tilapia':791,'tuna':792,'beer':793,'club_soda':794,'champagne':795,'gin':796,'juice':797,'mixers':798,'red_wine':799,'white_wine':800,'rum':801,'sake':802,'soda_pop':803,'sports_drink':804,'whiskey':805,'vodka':806,'bagels':807,'croissants':808,'buns':809,'cake':810,'cookies':811,'donuts':812,'pastries':813,'fresh_bread':814,'pie':815,'pita_bread':816,'sliced_bread':817,'baking_powder':818,'baking_soda':819,'bread_crumbs':820,'cake_mix':821,'brownie_mix':822,'cake_icing':823,'cake_decorations':824,'chocolate_chips/cocoa':825,'flour':826,'shortening':827,'sugar':828,'sugar_substitute':829,'yeast':830,'candy':831,'gum':832,'crackers':833,'dried_fruit':834,'granola_bars':835,'granola_mix':836,'nuts':837,'seeds':838,'oatmeal':839,'popcorn':840,'potato_chips':841,'corn_chips':842,'pretzels':843,'burger_night':844,'chili_night':845,'pizza_night':846,'spaghetti_night':847,'taco_night':848,'take-out_deli_food':849,'baby_food':850,'diapers':851,'formula':852,'lotion':853,'baby_wash':854,'wipes':855,'cat_food':856,'cat_treats':857,'cat_litter':858,'dog_food':859,'dog_treats':860,'flea_treatment':861,'pet_shampoo':862,'deodorant':863,'bath_soap':864,'hand_soap':865,'condoms':866,'cosmetics':867,'cotton_swabs':868,'cotton_balls':869,'facial_cleanser':870,'facial_tissue':871,'feminine_products':872,'floss':873,'hair_gel':874,'hair_spray':875,'lip_balm':876,'moisturizing_lotion':877,'mouthwash':878,'razors':879,'shaving_cream':880,'shampoo':881,'conditioner':882,'sunblock':883,'toilet_paper':884,'toothpaste':885,'vitamins':886,'supplements':887,'allergy':888,'antibiotic':889,'antidiarrheal':890,'aspirin':891,'antacid':892,'band-aids':893,'cold_/_flu':894,'pain_reliever':895,'prescription_pick-up':896,'aluminum_foil':897,'napkins':898,'non-stick_spray':899,'paper_towels':900,'plastic_wrap':901,'sandwich_/_freezer_bags':902,'wax_paper':903,'air_freshener':904,'bathroom_cleaner':905,'bleach':906,'detergent':907,'dish_/_dishwasher_soap':908,'garbage_bags':909,'glass_cleaner':910,'mop_head':911,'vacuum_bags':912,'sponges':913,'notepad':914,'envelopes':915,'glue':916,'tape':917,'printer_paper':918,'pens':919,'pencils':920,'postage_stamps':921,'arsenic':922,'asbestos':923,'cigarettes':924,'radionuclides':925,'vinyl_chloride':926}
    link = "https://www.mygrocerydeals.com/"
    stores_map = {'acme_markets':1,'jewel_osco':2,'lucky':3,'pavillions':4,'randalls':5,'tom_thumb':6,'safeway':7,'united_supermarkets':8,'market_street':9,'vons':10,'aldi':11,'costco':12,'kmart':13,'kroger':14,'schnucks':15,'food_lion':16,'hannaford':17,'giant':18,'stop_and_shop':19,'martins_food':20,'target':21,'trader_joes':22,'walmart':23,'whole_foods':24,'foodmaxx':25,'jewel-osco':2,'whole_foods_market':24,'super_stop_and_shop':19,'united_supermarket':8,'martins_food_markets':20,'giant_food':18,'giant_foods':18,'giant_food_stores':18,'walmart_supercenter':23,'walmart_neighborhood_market':23,'stop_&_shop':19,'super_stop_&_shop':19}
    #driver = webdriver.PhantomJS()
    no_sale_items = ['cat_treats', 'allergy', 'bath_soap','antacid', 'preserves', 'pens', 'sugar_substitute', 'cosmetics',  'bathroom_cleaner', 'razors', 'canned_veggies', 'baby_wash', 'dog_food', 'canned_tuna', 'candy', 'english_muffins', 'facial_cleanser', 'pizza_night', 'envelopes', 'facial_tissue', 'bleach', 'sandwich_/_freezer_bags', 'notepad', 'pet_shampoo', 'canned_chicken', 'taco_night', 'formula',  'postage_stamps', 'chili_night', 'bouillon_cubes', 'hand_soap', 'diapers', 'cotton_balls', 'floss', 'lotion', 'toilet_paper','condoms', 'sports_drink', 'salad_dressing','frozen_breakfasts', 'dish_/_dishwasher_soap', 'take-out_deli_food', 'sunblock', 'burger_night', 'toothpaste', 'canned_tomatoes', 'oregano','arsenic', 'air_freshener','cat_litter','shortening', 'sponges', 'garbage_bags', 'wipes', 'aspirin', 'tape', 'deodorant', 'moisturizing_lotion', 'vinegar', 'band-aids','flea_treatment', 'mop_head', 'vanilla_extract', 'mouthwash', 'tater_tots', 'fries', 'shampoo', 'canned_olives', 'tinned_meats', 'napkins',  'antidiarrheal', 'cold_/_flu', 'broth', 'tv_dinners', 'printer_paper', 'hair_spray', 'cat_food', 'aluminum_foil','hair_gel', 'instant_potatoes', 'plastic_wrap', 'packaged_meals', 'vacuum_bags', 'paper_towels','feminine_products', 'pain_reliever', 'pencils', 'radionuclides', 'shaving_cream', 'glass_cleaner', 'chip_dip', 'cigarettes', 'prescription_pick-up', 'fake_eggs',]

    weekday_list = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    # driver.get(link)
    # driver.find_element_by_id("q").send_keys("eggs")
    # driver.find_element_by_id("supplied_location").send_keys("95070")
    # print "set inputs"
    # search_btn = driver.find_element_by_xpath("//*[@id='form-search-deals']/div[3]/input")
    # search_btn.click()
    # sleep(1)
    # if driver.current_url == link:
    #     sleep(2)
    # print driver.current_url

    for nosaleitem in list(no_sale_items):
        if items_map.pop(nosaleitem,None) == None:
            no_sale_items.remove(nosaleitem)


    array = []
    # for name,id in items_map.iteritems():
    #     print name
    name = 'steak'
    r = requests.get("https://www.mygrocerydeals.com/deals?utf8=%E2%9C%93&authenticity_token=tRU5ntxShfoidDkK0M4K9O7K8e1qMh0q5Gn5w7HBBaLyIKfqVjB2tWpBgqedgZKl0JY51%2Fx9difRhAoFCqEWDg%3D%3D&remove%5B%5D=chains&remove%5B%5D=categories&remove%5B%5D=collection&remove%5B%5D=collection_id&q="+name+"&supplied_location=95070&latitude=42.300771&longitude=-71.400541")
    soup = BeautifulSoup(r.content,"html.parser")
    deals = soup.find_all('div', attrs={'class': 'deal'})

    if len(deals) != 0:
        for deal in deals:
            content = deal.find(attrs={'class':'tile-content'})
            supplier = content.find(attrs={'class': 'deal-storename'}).text.lstrip().lower().replace(" ", "_").replace(
                "-", "_").replace("'","")
            if supplier in stores_map:
                img_url =  content.find(attrs ={'class':'container-tile-image'}).find('img')['src']
                size = content.find(attrs ={'class':'container-tile-image'}).select('.uom')[0].text
                discount_type = content.find(attrs={'class':'pricetag'}).text
                if 'for' in discount_type:
                    digits = Decimal(re.findall(r"[-+]?\d*\.\d+|\d+", discount_type)[1])
                    discount = digits
                else:
                    discount = Decimal(re.sub(r"[^\d.]", '', discount_type))
                    discount_type = 'dollar_amount'
                item_name = content.find(attrs={'class':'deal-productname'}).text.lstrip()
                expiry_date = content.find(attrs={'class':'expirydate'}).text.replace("Ends ","")
                if "/" in expiry_date:
                    date_object = datetime.strptime(expiry_date, '%m/%d/%y')
                else:
                    d = datetime.today()
                    try:
                        weekday = weekday_list.index(expiry_date.lower().lstrip())
                        t = timedelta((7 + weekday - d.weekday()) % 7)
                        date_object = d + t
                        print (d+t).strftime('%m-%d-%Y')
                    except KeyError:
                        pass
                array.append({"id":id,"image_url":img_url,"size":size,"discount_type":discount_type,"discount":discount,'name':item_name,'supplier':supplier,
                              "end_date":date_object})


    for x in array:
        print x["discount_type"], x["discount"], x["end_date"]
    print ""

    #driver.quit()

def addAllItems():
    #copy this in python manage.py shell
    #creates itemtypes
    # to delete old entries - ItemType.objects.all().delete()

    string = "asparagus^vegetables,broccoli^vegetables,carrots^vegetables,cauliflower^vegetables,celery^vegetables,corn^vegetables,cucumbers^vegetables,lettuce^vegetables,mushrooms^vegetables,onions^vegetables,peppers^vegetables,potatoes^vegetables,spinach^vegetables,squash^vegetables,zucchini^vegetables,tomatoes^vegetables,apples^fruit,avocados^fruit,bananas^fruit,berries^fruit,cherries^fruit,grapefruit^fruit,grapes^fruit,kiwis^fruit,lemons^fruit,limes^fruit,melon^fruit,nectarines^fruit,oranges^fruit,peaches^fruit,pears^fruit,plums^fruit,chip_dip^refrigerated,eggs^refrigerated,fake_eggs^refrigerated,english_muffins^refrigerated,fruit_juice^refrigerated,hummus^refrigerated,ready-bake_breads^refrigerated,tofu^refrigerated,tortillas^refrigerated,frozen_breakfasts^frozen,frozen_burritos^frozen,fish_sticks^frozen,fries^frozen,tater_tots^frozen,ice_cream^frozen,sorbet^frozen,juice_concentrate^frozen,pizza^frozen,pizza_rolls^frozen,popsicles^frozen,tv_dinners^frozen,vegetables^frozen,bbq_sauce^condiments/sauces,gravy^condiments/sauces,honey^condiments/sauces,hot_sauce^condiments/sauces,jelly^condiments/sauces,jam^condiments/sauces,preserves^condiments/sauces,ketchup^condiments/sauces,mustard^condiments/sauces,mayonnaise^condiments/sauces,pasta_sauce^condiments/sauces,relish^condiments/sauces,salad_dressing^condiments/sauces,salsa^condiments/sauces,soy_sauce^condiments/sauces,steak_sauce^condiments/sauces,syrup^condiments/sauces,worcestershire_sauce^condiments/sauces,bouillon_cubes^various,cereal^various,coffee^various,coffee_filters^various,instant_potatoes^various,lemon_juice^various,lime_juice^various,mac_&_cheese^various,olive_oil^various,packaged_meals^various,pancake_mix^various,waffle_mix^various,pasta^various,peanut_butter^various,pickles^various,rice^various,tea^various,vegetable_oil^various,vinegar^various,applesauce^canned,baked_beans^canned,broth^canned,canned_fruit^canned,canned_olives^canned,tinned_meats^canned,canned_tuna^canned,canned_chicken^canned,canned_soup^canned,chili^canned,canned_tomatoes^canned,canned_veggies^canned,basil^spices & herbs,black_pepper^spices & herbs,cilantro^spices & herbs,cinnamon^spices & herbs,garlic^spices & herbs,ginger^spices & herbs,mint^spices & herbs,oregano^spices & herbs,paprika^spices & herbs,parsley^spices & herbs,red_pepper^spices & herbs,salt^spices & herbs,vanilla_extract^spices & herbs,butter^dairy,margarine^dairy,half_&_half^dairy,milk^dairy,sour_cream^dairy,whipped_cream^dairy,yogurt^dairy,bleu_cheese^cheese,cheddar^cheese,cottage_cheese^cheese,cream_cheese^cheese,feta^cheese,goat_cheese^cheese,mozzarella^cheese,parmesan^cheese,provolone^cheese,ricotta^cheese,sandwich_slices^cheese,swiss^cheese,bacon^meat,sausage^meat,beef^meat,steak^meat,chicken^meat,ground_beef^meat,turkey^meat,ham^meat,pork^meat,hot_dogs^meat,lunchmeat^meat,catfish^seafood,crab^seafood,lobster^seafood,mussels^seafood,oysters^seafood,salmon^seafood,shrimp^seafood,tilapia^seafood,tuna^seafood,beer^beverages,club_soda^beverages,champagne^beverages,gin^beverages,juice^beverages,mixers^beverages,red_wine^beverages,white_wine^beverages,rum^beverages,sake^beverages,soda_pop^beverages,sports_drink^beverages,whiskey^beverages,vodka^beverages,bagels^baked goods,croissants^baked goods,buns^baked goods,cake^baked goods,cookies^baked goods,donuts^baked goods,pastries^baked goods,fresh_bread^baked goods,pie^baked goods,pita_bread^baked goods,sliced_bread^baked goods,baking_powder^baking,baking_soda^baking,bread_crumbs^baking,cake_mix^baking,brownie_mix^baking,cake_icing^baking,cake_decorations^baking,chocolate_chips/cocoa^baking,flour^baking,shortening^baking,sugar^baking,sugar_substitute^baking,yeast^baking,candy^snacks,gum^snacks,crackers^snacks,dried_fruit^snacks,granola_bars^snacks,granola_mix^snacks,nuts^snacks,seeds^snacks,oatmeal^snacks,popcorn^snacks,potato_chips^snacks,corn_chips^snacks,pretzels^snacks,burger_night^themed meals,chili_night^themed meals,pizza_night^themed meals,spaghetti_night^themed meals,taco_night^themed meals,take-out_deli_food^themed meals,baby_food^baby,diapers^baby,formula^baby,lotion^baby,baby_wash^baby,wipes^baby,cat_food^pets,cat_treats^pets,cat_litter^pets,dog_food^pets,dog_treats^pets,flea_treatment^pets,pet_shampoo^pets,deodorant^care,bath_soap^care,hand_soap^care,condoms^care,cosmetics^care,cotton_swabs^care,cotton_balls^care,facial_cleanser^care,facial_tissue^care,feminine_products^care,floss^care,hair_gel^care,hair_spray^care,lip_balm^care,moisturizing_lotion^care,mouthwash^care,razors^care,shaving_cream^care,shampoo^care,conditioner^care,sunblock^care,toilet_paper^care,toothpaste^care,vitamins^care,supplements^care,allergy^medicine,antibiotic^medicine,antidiarrheal^medicine,aspirin^medicine,antacid^medicine,band-aids^medicine,cold_/_flu^medicine,pain_reliever^medicine,prescription_pick-up^medicine,aluminum_foil^kitchen,napkins^kitchen,non-stick_spray^kitchen,paper_towels^kitchen,plastic_wrap^kitchen,sandwich_/_freezer_bags^kitchen,wax_paper^kitchen,air_freshener^cleaning,bathroom_cleaner^cleaning,bleach_^cleaning,detergent^cleaning,dish_/_dishwasher_soap^cleaning,garbage_bags^cleaning,glass_cleaner^cleaning,mop_head^cleaning,vacuum_bags^cleaning,sponges^cleaning,notepad^supply,envelopes^supply,glue^supply,tape^supply,printer_paper^supply,pens^supply,pencils^supply,postage_stamps^supply,arsenic^carcinogens,asbestos^carcinogens,cigarettes^carcinogens,radionuclides^carcinogens,vinyl_chloride^carcinogens"
    items = string.split(",")
    for item in items:
        arry = item.split("^")
        name = arry[0]
        category = arry[1]
        try:
            print name
            new_item = ItemType(name=name,category=category,typical_price=0)
            new_item.save()
        except Exception:
            print name


def addAllStores():
    string = "acme_markets,jewel_osco,lucky,pavillions,randalls,tom_thumb,safeway,united_supermarkets,market_street,vons,aldi,costco,kmart,kroger,schnucks,food_lion,hannaford,giant_food_stores,stop_and_shop,martins_food,target,trader_joes,walmart,whole_foods"
    stores = string.split(",")
    for name in stores:
        store = Supplier(name=name)
        store.save()
def getItemNameandID():
    total = ""
    items = ItemType.objects.all()
    for item in items:
        total = total + str(item.pk) + "^" + item.name + ","
    print total
def getMap():
    total = "{"
    items = Supplier.objects.all()
    alias = SupplierAlias.objects.all()
    for item in items:
        total = total + "'" +item.name + "':" + str(item.pk) +","
    for x in alias:
        total = total + "'" +x.alias + "':" + str(x.supplier.pk) +","
    print total


def findDuplicates():
    string = "asparagus^vegetables,broccoli^vegetables,carrots^vegetables,cauliflower^vegetables,celery^vegetables,corn^vegetables,cucumbers^vegetables,lettuce^vegetables,mushrooms^vegetables,onions^vegetables,peppers^vegetables,potatoes^vegetables,spinach^vegetables,squash^vegetables,zucchini^vegetables,tomatoes^vegetables,apples^fruit,avocados^fruit,bananas^fruit,berries^fruit,cherries^fruit,grapefruit^fruit,grapes^fruit,kiwis^fruit,lemons^fruit,limes^fruit,melon^fruit,nectarines^fruit,oranges^fruit,peaches^fruit,pears^fruit,plums^fruit,chip_dip^refrigerated,eggs^refrigerated,fake_eggs^refrigerated,english_muffins^refrigerated,fruit_juice^refrigerated,hummus^refrigerated,ready-bake_breads^refrigerated,tofu^refrigerated,tortillas^refrigerated,frozen_breakfasts^frozen,frozen_burritos^frozen,fish_sticks^frozen,fries^frozen,tater_tots^frozen,ice_cream^frozen,sorbet^frozen,juice_concentrate^frozen,pizza^frozen,pizza_rolls^frozen,popsicles^frozen,tv_dinners^frozen,vegetables^frozen,bbq_sauce^condiments/sauces,gravy^condiments/sauces,honey^condiments/sauces,hot_sauce^condiments/sauces,jelly^condiments/sauces,jam^condiments/sauces,preserves^condiments/sauces,ketchup^condiments/sauces,mustard^condiments/sauces,mayonnaise^condiments/sauces,pasta_sauce^condiments/sauces,relish^condiments/sauces,salad_dressing^condiments/sauces,salsa^condiments/sauces,soy_sauce^condiments/sauces,steak_sauce^condiments/sauces,syrup^condiments/sauces,worcestershire_sauce^condiments/sauces,bouillon_cubes^various,cereal^various,coffee^various,coffee_filters^various,instant_potatoes^various,lemon_juice^various,lime_juice^various,mac_&_cheese^various,olive_oil^various,packaged_meals^various,pancake_mix^various,waffle_mix^various,pasta^various,peanut_butter^various,pickles^various,rice^various,tea^various,vegetable_oil^various,vinegar^various,applesauce^canned,baked_beans^canned,broth^canned,canned_fruit^canned,canned_olives^canned,tinned_meats^canned,canned_tuna^canned,canned_chicken^canned,canned_soup^canned,chili^canned,canned_tomatoes^canned,canned_veggies^canned,basil^spices & herbs,black_pepper^spices & herbs,cilantro^spices & herbs,cinnamon^spices & herbs,garlic^spices & herbs,ginger^spices & herbs,mint^spices & herbs,oregano^spices & herbs,paprika^spices & herbs,parsley^spices & herbs,red_pepper^spices & herbs,salt^spices & herbs,vanilla_extract^spices & herbs,butter^dairy,margarine^dairy,half_&_half^dairy,milk^dairy,sour_cream^dairy,whipped_cream^dairy,yogurt^dairy,bleu_cheese^cheese,cheddar^cheese,cottage_cheese^cheese,cream_cheese^cheese,feta^cheese,goat_cheese^cheese,mozzarella^cheese,parmesan^cheese,provolone^cheese,ricotta^cheese,sandwich_slices^cheese,swiss^cheese,bacon^meat,sausage^meat,beef^meat,steak^meat,chicken^meat,ground_beef^meat,turkey^meat,ham^meat,pork^meat,hot_dogs^meat,lunchmeat^meat,catfish^seafood,crab^seafood,lobster^seafood,mussels^seafood,oysters^seafood,salmon^seafood,shrimp^seafood,tilapia^seafood,tuna^seafood,beer^beverages,club_soda^beverages,champagne^beverages,gin^beverages,juice^beverages,mixers^beverages,red_wine^beverages,white_wine^beverages,rum^beverages,sake^beverages,soda_pop^beverages,sports_drink^beverages,whiskey^beverages,vodka^beverages,bagels^baked goods,croissants^baked goods,buns^baked goods,cake^baked goods,cookies^baked goods,donuts^baked goods,pastries^baked goods,fresh_bread^baked goods,pie^baked goods,pita_bread^baked goods,sliced_bread^baked goods,baking_powder^baking,baking_soda^baking,bread_crumbs^baking,cake_mix^baking,brownie_mix^baking,cake_icing^baking,cake_decorations^baking,chocolate_chips/cocoa^baking,flour^baking,shortening^baking,sugar^baking,sugar_substitute^baking,yeast^baking,candy^snacks,gum^snacks,crackers^snacks,dried_fruit^snacks,granola_bars^snacks,granola_mix^snacks,nuts^snacks,seeds^snacks,oatmeal^snacks,popcorn^snacks,potato_chips^snacks,corn_chips^snacks,pretzels^snacks,burger_night^themed meals,chili_night^themed meals,pizza_night^themed meals,spaghetti_night^themed meals,taco_night^themed meals,take-out_deli_food^themed meals,baby_food^baby,diapers^baby,formula^baby,lotion^baby,baby_wash^baby,wipes^baby,cat_food^pets,cat_treats^pets,cat_litter^pets,dog_food^pets,dog_treats^pets,flea_treatment^pets,pet_shampoo^pets,deodorant^care,bath_soap^care,hand_soap^care,condoms^care,cosmetics^care,cotton_swabs^care,cotton_balls^care,facial_cleanser^care,facial_tissue^care,feminine_products^care,floss^care,hair_gel^care,hair_spray^care,lip_balm^care,moisturizing_lotion^care,mouthwash^care,razors^care,shaving_cream^care,shampoo^care,conditioner^care,sunblock^care,toilet_paper^care,toothpaste^care,vitamins^care,supplements^care,allergy^medicine,antibiotic^medicine,antidiarrheal^medicine,aspirin^medicine,antacid^medicine,band-aids^medicine,cold_/_flu^medicine,pain_reliever^medicine,prescription_pick-up^medicine,aluminum_foil^kitchen,napkins^kitchen,non-stick_spray^kitchen,paper_towels^kitchen,plastic_wrap^kitchen,sandwich_/_freezer_bags^kitchen,wax_paper^kitchen,air_freshener^cleaning,bathroom_cleaner^cleaning,bleach_^cleaning,detergent^cleaning,dish_/_dishwasher_soap^cleaning,garbage_bags^cleaning,glass_cleaner^cleaning,mop_head^cleaning,vacuum_bags^cleaning,sponges^cleaning,notepad^supply,envelopes^supply,glue^supply,tape^supply,printer_paper^supply,pens^supply,pencils^supply,postage_stamps^supply,arsenic^carcinogens,asbestos^carcinogens,cigarettes^carcinogens,radionuclides^carcinogens,vinyl_chloride^carcinogens,"
    items = string.split(",")
    array = []
    for item in items:
        arry = item.split("^")
        name = arry[0]
        array.append(name)
    print set([x for x in array if array.count(x) > 1])

if __name__ == "__main__": main()
