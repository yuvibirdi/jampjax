class_name GUI
extends CanvasLayer

@onready var _jack_label: Label = get_node("HSplitContainer/Container/Label")

func update_jacks(new_jacks):
	_jack_label.text = str(new_jacks) + " Jacks"
