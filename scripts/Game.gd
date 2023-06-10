class_name Game
extends Node

var _jack: Jack
var _owned_upgrades: Dictionary
var _jacks = 0
var _jack_count_label: Label
var _udp := PacketPeerUDP.new()

var _upgrades := [
	Upgrade.new("Test", 1, 0.1)
]

func _ready():
	_jack = get_node("%Jack")
	_jack_count_label = get_node("HSplitContainer/Container/Label")
	
	var store_container = load("res://templates/StoreItem.tscn")
	for upgrade in _upgrades:
		var item = store_container.instantiate()
		item.setup(upgrade)
		get_node("HSplitContainer/Store/ScrollContainer/VBoxContainer").add_child(item)
		_owned_upgrades[upgrade] = 0
		
	_udp.bind(5005, "0.0.0.0")
	var udp_thread = Thread.new()
	udp_thread.start(udp_reciever)

func click():
	_jacks += 1
	_jack.pulse()
	_jack_count_label.text = str(_jacks) + " Jacks"

func mouse_down():
	_jack.down()

func get_jacks():
	return _jacks

func purchase(upgrade: Upgrade):
	_jacks -= upgrade.get_price()
	_jack_count_label.text = str(_jacks) + " Jacks"
	_owned_upgrades[upgrade] += 1
	upgrade.purchase()

func udp_reciever():
	while _udp.wait() == OK:
		var data = _udp.get_packet().get_string_from_ascii()
		print(data)
		if data == "Jumping Jack":
			click()
