class_name Game
extends Node

var _jack: Jack
var _owned_upgrades: Dictionary
var _jacks = 0
var _jack_count_label: Label
var _udp := PacketPeerUDP.new()
var _energy = 0
var _energy_bar: ProgressBar

var _upgrades := [
	Upgrade.new("More Jack", 5, 0.5),
	Upgrade.new("Energizer", 5, 1),
	Upgrade.new("Trainee Jack", 10, 1),
	Upgrade.new("Super Jack", 100, 0.5)
]

func _ready():
	_jack = get_node("%Jack")
	_jack_count_label = get_node("HSplitContainer/Container/Label")
	_energy_bar = get_node("HSplitContainer/Container/Energy")
	
	var store_container = load("res://templates/StoreItem.tscn")
	for upgrade in _upgrades:
		var item = store_container.instantiate()
		item.setup(upgrade)
		get_node("HSplitContainer/Store/Store/ScrollContainer/VBoxContainer").add_child(item)
		_owned_upgrades[upgrade] = 0
		
	_udp.bind(5005, "0.0.0.0")
	var udp_thread = Thread.new()
	udp_thread.start(udp_reciever)
	
var timer = 0
func _process(delta: float) -> void:
	if (_energy > 0 && timer >= 1):
		_energy -= 1
		_jacks += _owned_upgrades[_upgrades[2]] # Trainee: 1/s
		_jacks += _owned_upgrades[_upgrades[3]] # Super: 10/s
		timer -= 1
		_jack_count_label.text = str(_jacks) + " Jacks"
	_energy_bar.value = clamp(_energy, 0, 100)
	timer += delta
		
	if (Input.is_action_just_pressed("click")):
		click()
	if (Input.is_action_just_pressed("alt_click")):
		energize()

func click():
	_jacks += 1 + _owned_upgrades[_upgrades[0]]
	_jack.pulse()
	_jack_count_label.text = str(_jacks) + " Jacks"
	
func energize():
	_energy += 1 + _owned_upgrades[_upgrades[1]]

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
		match data:
			"Jumping Jack":
				click()
			"Squat":
				energize()
			"High Knee":
				energize()
