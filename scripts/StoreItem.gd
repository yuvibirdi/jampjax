class_name StoreItem
extends TextureButton

@onready
var _price_label = get_node("Container/Price")
@onready
var _owned_label = get_node("Owned")
@onready
var _game = get_node("/root/Game")

var upgrade: Upgrade

func setup(upgrade: Upgrade):
	self.upgrade = upgrade

func _ready():
	get_node("Container/Name").text = upgrade.get_item_name()
	_price_label.text = str(upgrade.get_price())
	get_node("Icon").texture = load("res://assets/upgrades/" + upgrade.get_item_name() + ".png")
	update_owned(0)

func _process(delta):
	set_disabled(_game.get_jacks() < upgrade.get_price())
	
func update_owned(owned: int):
	_owned_label.text = str(owned)

func _on_pressed() -> void:
	_game.purchase(upgrade)
	update_owned(upgrade.get_owned())
	_price_label.text = str(upgrade.get_price())
