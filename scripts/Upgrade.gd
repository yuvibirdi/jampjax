class_name Upgrade
extends TextureButton

var _name: String
var _price: int
var _price_multiplier: float
var _owned := 0

func _init(name: String, price: int, multiplier: float):
	_name = name
	_price = price
	_price_multiplier = multiplier

func purchase():
	_owned += 1
	
func get_item_name() -> String:
	return _name

func get_price() -> int:
	return _price + _price * _price_multiplier * _owned

func get_owned() -> int:
	return _owned
