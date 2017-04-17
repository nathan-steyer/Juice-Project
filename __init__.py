from flask import Flask, render_template
import requests, json, re

query = {}
query['appId'] = 'd704c37f'
query['appKey'] = '9d94b5b51ccfb1cf5f8dc3ac208cbdbc'
query['fields'] = [
	'item_name',
	'nf_calories',
	'nf_serving_size_qty',
	'nf_serving_size_unit',
	'nf_ingredient_statement'
]
query['offset'] = 0
query['limit'] = 50

sort = {}
sort['field'] = 'item_name'
sort['order'] = 'asc'
query['sort'] = sort

filters = {}
filters['brand_id'] = '51db37d0176fe9790a899db2'
query['filters'] = filters


url = 'https://api.nutritionix.com/v1_1/search'
headers = { 'Content-Type': 'application/json' }
response = requests.post(url, headers=headers, data=json.dumps(query)).json()
hits = response['hits']

while len(hits) < response['total']:
	query['offset'] = len(hits)
	response = requests.post(url, headers=headers, data=json.dumps(query)).json()
	hits += response['hits']

totalProducts = len(hits)

ingredientNames = [
	('Apple Juice', re.compile('apple(?<!pine)', re.IGNORECASE)),
	('Pear Juice', re.compile('pear', re.IGNORECASE)),
	('Grape Juice', re.compile('grape(?<!white )', re.IGNORECASE)),
	('Raspberry Juice', re.compile('ra(?:ps|sp)berry', re.IGNORECASE)),
	('Orange Juice', re.compile('orange', re.IGNORECASE)),
	('Tangerine Juice', re.compile('tangerine', re.IGNORECASE)),
	('White Grape Juice', re.compile('white', re.IGNORECASE)),
	('Strawberry Juice', re.compile('strawberry', re.IGNORECASE)),
	('Pineapple Juice', re.compile('pineapple', re.IGNORECASE)),
	('Watermelon Juice', re.compile('watermelon', re.IGNORECASE)),
	('Kiwi Juice', re.compile('kiwi', re.IGNORECASE)),
	('Cherry Juice', re.compile('cherry', re.IGNORECASE)),
	('Carrot Juice', re.compile('carrot', re.IGNORECASE)),
	('Passion Fruit Juice', re.compile('passion', re.IGNORECASE)),
	('Lemon Juice', re.compile('lemon', re.IGNORECASE)),
	('Cranberry Juice', re.compile('cranberry', re.IGNORECASE)),
	('Peach Juice', re.compile('peach juice', re.IGNORECASE)),
	('Vegetable Juice', re.compile('vegetable', re.IGNORECASE)),
	('Mango Puree', re.compile('mango', re.IGNORECASE)),
	('Banana Puree', re.compile('banana', re.IGNORECASE)),
	('Sweet Potato Puree', re.compile('potato', re.IGNORECASE)),
	('Peach Puree', re.compile('peach puree', re.IGNORECASE)),
	('Natural Flavors', re.compile('natural', re.IGNORECASE)),
	('Carbonation', re.compile('carbonation', re.IGNORECASE)),
	('Pectin', re.compile('pectin', re.IGNORECASE)),
	('Fish Oil', re.compile('fish', re.IGNORECASE)),
	('Gellan Gum', re.compile('gellan', re.IGNORECASE)),
	('Gum Acacia', re.compile('acacia', re.IGNORECASE)),
	('Beta Carotene', re.compile('carotene', re.IGNORECASE)),
	('Zinc Gluconate', re.compile('zinc', re.IGNORECASE)),
	('Ascorbic Acid', re.compile('ascorbic', re.IGNORECASE)),
	('Citric Acid', re.compile('citric', re.IGNORECASE)),
	('Malic Acid', re.compile('malic', re.IGNORECASE))
]

flavorNames = [
	('Apple Raspberry', re.compile('apple raspberry', re.IGNORECASE)),
	('Apple Banana', re.compile('apple banana', re.IGNORECASE)),
	('Apple Frenzy', re.compile('apple frenzy', re.IGNORECASE)),
	('Apple Quench', re.compile('apple quench', re.IGNORECASE)),
	('Apple Grape', re.compile('apple grape', re.IGNORECASE)),
	('Cranberry Apple', re.compile('cranberry apple', re.IGNORECASE)),
	('Orange Tangerine', re.compile('orange tangerine', re.IGNORECASE)),
	('Orange Mango', re.compile('orange mango', re.IGNORECASE)),
	('Strawberry Watermelon', re.compile('strawberry watermelon', re.IGNORECASE)),
	('Strawberry Banana', re.compile('strawberry banana', re.IGNORECASE)),
	('Kiwi Strawberry', re.compile('kiwi strawberry', re.IGNORECASE)),
	('Watermelon Madness', re.compile('watermelon madness', re.IGNORECASE)),
	('Orange Strawbana Blast', re.compile('orange strawbana blast', re.IGNORECASE)),
	('Wild Cherry Craze', re.compile('wild cherry craze', re.IGNORECASE)),
	('Berry Lemon Blast', re.compile('berry lemon blast', re.IGNORECASE)),
	('Berry Cherry Burst', re.compile('berry cherry burst', re.IGNORECASE)),
	('Sparkling Berry', re.compile('sparkling berry', re.IGNORECASE)),
	('Sparkling Orange', re.compile('sparkling orange', re.IGNORECASE)),
	('Sparkling Apple', re.compile('sparkling apple', re.IGNORECASE)),
	('Tropical Punch', re.compile('tropical punch', re.IGNORECASE)),
	('Fruit Punch', re.compile('fruit punch', re.IGNORECASE)),
	('Punch Splash', re.compile('punch splash', re.IGNORECASE)),
	('Strawberry', re.compile('strawberry', re.IGNORECASE)),
	('White Grape', re.compile('white grape', re.IGNORECASE)),
	('Watermelon', re.compile('watermelon', re.IGNORECASE)),
	('Tropical', re.compile('tropical', re.IGNORECASE)),
	('Punch', re.compile('punch', re.IGNORECASE)),
	('Apple', re.compile('apple', re.IGNORECASE)),
	('Grape', re.compile('grape', re.IGNORECASE)),
	('Mango', re.compile('mango', re.IGNORECASE)),
	('Berry', re.compile('berry', re.IGNORECASE)),
	('Cherry', re.compile('cherry', re.IGNORECASE)),
	('Peach', re.compile('peach', re.IGNORECASE))
]


calories = 0
ounces = 0
ingredientsMap = {}

for hit in hits:
	info = hit['fields']
	ingredients = info['nf_ingredient_statement']
	
	if info['nf_serving_size_unit'] == 'fl oz':
		calories += info['nf_calories']
		ounces += info['nf_serving_size_qty']
	
	if ingredients is not None:
		cleanIngredients = []
		
		for pair in ingredientNames:
			name = pair[0]
			regExpr = pair[1]
			if regExpr.search(ingredients) is not None:
				cleanIngredients.append(name)
		
		for pair in flavorNames:
			name = pair[0]
			regExpr = pair[1]
			if regExpr.search(info['item_name']) is not None:
				cleanName = name
				break
		
		for cleanIngredient in cleanIngredients:
			if cleanIngredient in ingredientsMap:
				ingredientsMap[cleanIngredient].add(cleanName)
			else:
				ingredientsMap[cleanIngredient] = {cleanName}

caloriesPerOunce = calories / ounces


app = Flask(__name__)

@app.route('/')
@app.route('/<ingredient>')
def send_page(ingredient=None):
	return render_template('base.html', map=ingredientsMap, clicked=ingredient)

@app.route('/total')
def send_total():
	response = {}
	response['total_products'] = totalProducts
	return json.dumps(response)

@app.route('/average')
def send_average():
	response = {}
	response['average_calories_per_fl_oz'] = caloriesPerOunce
	return json.dumps(response)