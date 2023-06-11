extends ProgressBar

var _energy_increase = preload("res://templates/EnergyIncrease.tscn")
var _last_value = 0

@onready
var _rng = RandomNumberGenerator.new()

func _on_value_changed(value: float) -> void:
	if value > _last_value:
		print("Added")
		var instance = _energy_increase.instantiate()
		instance.position = Vector2(_rng.randi_range(0, 1920/2), 0)
		add_child(instance)
	_last_value = value
	
