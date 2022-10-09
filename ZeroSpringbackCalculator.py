import numpy as np

# Test Data for 2.9mm mandrel_x = 4.426, mandrel_y = 4.086,
# mandrel_gap = 3.3, pin_radius = 14.978, mandrel_dia = 5.8


def zero_springback_calc(wire_dia, mandrel_x, mandrel_y, mandrel_gap, pin_radius, mandrel_dia):
	'''
	Function to generate the data for a Zero Springback material
	profile for DI Wire Pro machines.

	User inputs Wire Diameter, Mandrel X Location, Mandrel Y Location,
	Mandrel Gap, Pin Radius from Center, and Mandrel ID.

	Note: The final ccw value will have a comma that must be removed

	Written by Mason Goodson
	'''

	mandrel_pos = np.array([mandrel_x, mandrel_y])

	mandrel_angle = np.degrees(np.arctan(mandrel_x/mandrel_y))

	# Determine Pin Angle at Zero Degree Bend
	pin_angle_at_zero = round(np.degrees(-np.arcsin(((mandrel_dia/2)+(wire_dia/2)-(mandrel_gap-wire_dia)/2)/pin_radius)), 2)

	angle_array = [[pin_angle_at_zero, 0]]

	# Math to determing the pin angle vs wire angle relationship
	while angle_array[len(angle_array)-1][1] < 200:
		current_angle = angle_array[len(angle_array)-1][0] + 10
		
		pin_pos = np.array([pin_radius * np.sin(np.deg2rad(current_angle)), pin_radius * np.cos(np.deg2rad(current_angle))])
		
		mandrel_to_pin = pin_pos - mandrel_pos
		
		mandrel_to_pin_length = np.sqrt(np.square(pin_pos[0]-mandrel_pos[0])+np.square(pin_pos[1]-mandrel_pos[1]))
		
		if current_angle <= mandrel_angle:
			mandrel_pos_unit_vector = mandrel_pos / np.linalg.norm(mandrel_pos)
			mandrel_to_pin_unit_vector = mandrel_to_pin / np.linalg.norm(mandrel_to_pin)
			dot_product = np.dot(mandrel_pos_unit_vector, mandrel_to_pin_unit_vector)
			mandrel_to_pin_angle = 180 - np.degrees(np.arccos(dot_product))
			
			mandrel_to_wire_angle = np.degrees(np.arcsin((mandrel_dia/2+wire_dia/2)/(mandrel_to_pin_length/2)))
			
			wire_angle = 180 - (360 - mandrel_angle - mandrel_to_pin_angle - mandrel_to_wire_angle)
		
			angle_array.append([current_angle, wire_angle])
		else:
			mandrel_pos_unit_vector = mandrel_pos / np.linalg.norm(mandrel_pos)
			mandrel_to_pin_unit_vector = mandrel_to_pin / np.linalg.norm(mandrel_to_pin)
			dot_product = np.dot(mandrel_pos_unit_vector, mandrel_to_pin_unit_vector)
			mandrel_to_pin_angle = 360 - (180 - np.degrees(np.arccos(dot_product)))
			
			mandrel_to_wire_angle = np.degrees(np.arcsin((mandrel_dia/2+wire_dia/2)/(mandrel_to_pin_length/2)))
			
			wire_angle = 180 - (360 - mandrel_angle - mandrel_to_pin_angle - mandrel_to_wire_angle)
			
			if wire_angle > 200:
				break
			else:
				angle_array.append([current_angle, wire_angle])

	print(angle_array)

	# Format output to text that can be copied directly to the mateial profile file
	count = 0
	for angles in angle_array:
		print(f'            \"{str(count)}-cw\": {str(round(angle_array[count][1],2))},')
		count += 1
	first_count = count
	
	for angles in angle_array:
		print(f'            \"{str(count)}-ccw\": {str(round(angle_array[count-first_count][1],2))},')
		count += 1

if __name__ == '__main__':
	wire_dia = float(input('Input Wire Diameter in mm: '))
	mandrel_x = float(input('Input Mandrel X Position in mm: '))
	mandrel_y = float(input('Input Mandrel Y Position in mm: '))
	mandrel_gap = float(input('Input Mandrel Gap in mm: '))
	pin_radius = float(input('Input Pin Radius in mm: '))
	mandrel_dia = float(input('Input Mandrel/Pin Diameter in mm: '))	
	
	zero_springback_calc(wire_dia, mandrel_x, mandrel_y,	mandrel_gap,	pin_radius, mandrel_dia)