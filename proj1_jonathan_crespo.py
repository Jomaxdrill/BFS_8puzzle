from collections import deque
import numpy as np

#*For store a given configuration of the puzzle the following tuple structure is defined:
#?(state, index, parent)

def to_string_sequence(sequence):
	seq_string = str(sequence)
	#*when the zero is first in the sequence, it is lost
	#*so it must be retrieved
	if len(seq_string) != 9:
		seq_string = '0' + seq_string
	return seq_string
def to_matrix(sequence):
	"""
	Converts the integer sequence that represents the state (where each digit is a tile of the puzzle) into a matrix
	for operate through actions.
	Args:
		sequence (number): Integer representing the state of the puzzle in column wise format

	Returns:
		array: 3x3 string matrix representing  each cell a number/tile of the puzzle
	"""
	sequence_string = to_string_sequence(sequence)
	matrix_form = np.array([ list(sequence_string[0:3]), list(sequence_string[3:6]), list(sequence_string[6:9]) ])
	matrix_form = np.transpose(matrix_form)
	return matrix_form
def to_sequence(matrix):
	"""
	Converts the 3x3 matrix to an integer sequence where each digit is a tile of the puzzle

	Args:
		matrix (array): 3x3 string matrix representing  each cell a number/tile of the puzzle

	Returns:
		number: integer representing the state of the puzzle in column wise format
	"""
	#to avoid a warning about element wise operation as the matrix from
	#input user elements will be integers, not string and plus join doesn't work if elements are arrays of numbers
	mtrx = np.array([  [str(element) for element in row]  for row in matrix ])
	return int( f'{"".join(mtrx[0:3,0])}{"".join(mtrx[0:3,1])}{"".join(mtrx[0:3,2])}' )
def input_matrix(name):
	"""Command User Interface to input initial and goal state matrices

	Args:
		name (str): Name of the 3x3 matrix to create and fill

	Raises:
		Exception: NotExactElements
		Exception: NumbersNotValid
		Exception: ElementAlready
		Exception: ValueError

	Returns:
		array: a 3x3 matrix composed of elements from 0 to 8 with no duplicates
	"""
	matrix_provided = False
	matrix = []
	while not matrix_provided:
		matrix = []
		print(f'Enter { name } state:\n Remember it is required nine numbers from 0 to 8 ( 0 is the blank tile ).\n No duplicates allowed!!\n')
		try:
			for idx in range(3):
				input_row = input(f'Write the first 3 numbers of row { idx + 1 } for { name } state separated by comma ( eg: 1,2,3 ).')
				row_process = input_row.split(',')
				row_process = [ int(element) for element in row_process ]
				#*set class for automatically check duplicates on the input
				check_duplicates = set(row_process)
				if len(check_duplicates) != 3:
					raise Exception('NotExactElements')
				#check user input numbers between 0 and 8
				number_out_bounds = False
				for element in row_process:
					if not (element >= 0 and element <= 8):
						number_out_bounds = True
						break
				if number_out_bounds:
					raise Exception('NumbersNotValid')
				#*check if user didn't repeat a value before
				element_already = False
				#comtemplating when it should already a number that was input before
				if len(matrix):
					for element in row_process:
						is_here = np.where(np.array(matrix) == element)
						if len(is_here[0]):
							element_already = True
							break
				if element_already:
					raise Exception('ElementAlready')
				print(f'The row { idx + 1 } is : { row_process }\n')
				confirm = input('Confirm row? (y/n): ')
				if confirm == 'y':
					matrix.append(row_process)
				else:
					print('Must write state again')
					raise Exception('Repeat')
		except ValueError as error:
			print(error)
			print(f'Invalid input for the row. Could not convert to integer all values.')
			break
		except Exception as err:
			args = err.args
			if 'NotExactElements' in args:
				print('im here')
				print('The total of numbers is not 3. Please try again.')
				break
			elif 'ElementAlready' in args:
				print('One Element provided is already given. Please try again.')
				break
			elif 'NumbersNotValid' in args:
				print('One Element/Number is not valid. Please try again.')
				break
			else:
				print(err)
				break
		matrix_provided = True
	if matrix_provided:
		print(f'{ name } State is:\n ')
		print(*[str(row).strip() + '\n' for row in matrix])
		return matrix
	else:
		return input_matrix(name)

def find_blank_tile(node_state):
	""" Searchs for the index of the element 0 in the node matrix state

	Args:
		node_state (array): the current state of the node

	Returns:
		tuple: the position of the blank tile in the node state
	"""
	blank_tile_index = np.where(node_state == '0')
	(i, j) = blank_tile_index[0][0], blank_tile_index[1][0]
	return i, j

def action_move_left(current_node):
	"""
	Args:
		current_node (Node): Node to move left its tile (number 0)

	Returns:
		Node: new Node with new configuration and state
	"""
	matrix_form = to_matrix(current_node[0])
	(i_blank, j_blank) = find_blank_tile(matrix_form)
	if j_blank - 1 >= 0:
		state_moved_left = np.copy(matrix_form)
		state_moved_left[i_blank][j_blank] = state_moved_left[i_blank][j_blank-1]
		state_moved_left[i_blank][j_blank-1] = '0'
		new_node = ( to_sequence(state_moved_left), -1, current_node[1] )
		return new_node
	return None
def action_move_right(current_node):
	"""
	Args:
		current_node (Node): Node to move right its tile (number 0)

	Returns:
		Node: new Node with new configuration and state
	"""
	matrix_form = to_matrix(current_node[0])
	(i_blank, j_blank) = find_blank_tile(matrix_form)
	if j_blank + 1 <= 2:
		state_moved_right = np.copy(matrix_form)
		state_moved_right[i_blank][j_blank] = state_moved_right[i_blank][j_blank+1]
		state_moved_right[i_blank][j_blank+1] = '0'
		new_node = ( to_sequence(state_moved_right), -1, current_node[1] )
		return new_node
	return None

def action_move_up(current_node):
	"""

	Args:
		current_node (Node): Node to move up its tile (number 0)

	Returns:
		Node: new Node with new configuration and state
	"""
	matrix_form = to_matrix(current_node[0])
	(i_blank, j_blank) = find_blank_tile(matrix_form)
	if i_blank - 1 >= 0:
		state_moved_up = np.copy(matrix_form)
		state_moved_up[i_blank][j_blank] = state_moved_up[i_blank-1][j_blank]
		state_moved_up[i_blank-1][j_blank] = '0'
		new_node = ( to_sequence(state_moved_up), -1, current_node[1] )
		return new_node
	return None

def action_move_down(current_node):
	"""

	Args:
		current_node (Node): Node to move down its tile (number 0)

	Returns:
		Node: new Node with new configuration and state
	"""
	matrix_form = to_matrix(current_node[0])
	(i_blank, j_blank) = find_blank_tile(matrix_form)
	if i_blank + 1 <= 2:
		state_moved_down = np.copy(matrix_form)
		state_moved_down[i_blank][j_blank] = state_moved_down[i_blank+1][j_blank]
		state_moved_down[i_blank+1][j_blank] = '0'
		new_node = ( to_sequence(state_moved_down), -1, current_node[1] )
		return new_node
	return None

def apply_action_set(node):
	"""Applies the full action set of possible moves

	Args:
		node (Node): Node to apply the actions set

	Returns:
		array: outputs of the actions applied, if the action was not possible the element will be None
	"""
	node_l = action_move_left(node)
	node_u = action_move_up(node)
	node_r = action_move_right(node)
	node_d = action_move_down(node)
	return [node_l, node_u, node_r, node_d]

def create_nodes(initial_state, goal_state):
	"""Creates the State space of all possible movements until goal state is reached.

	Args:
		initial_state (array): multi dimensional array 3x3 that describes the initial configuarion of the puzzle
		goal_state (array): multi dimensional array 3x3 that describes the final configuration the algorithm must find.

	Returns:
		str: 'DONE'. The process have ended thus we have a solution in the tree structure generated.
	"""
	goal_reached = False
	goal_node = to_sequence(goal_state)
	#*add root node to the queue
	generated_nodes.append(( to_sequence(initial_state), 0, None ) )
	counter_nodes = 0
	while not goal_reached:
		print(counter_nodes)
		#store it into a variable
		current_node = generated_nodes[0]
		#mark node as visited
		visited_nodes.append(current_node)
		visited_nodes_states.update([current_node[0]])
		#remove it from the queue
		generated_nodes.popleft()
		#apply action set to node to get new states/childrens
		child_nodes = apply_action_set(current_node)
		for child in child_nodes:
			#*if movement was not possible ignore it
			if not child:
				continue
			#check if child is goal state
			if child[0] == goal_node:
				last_child = (child[0], len(visited_nodes), child[2])
				visited_nodes.append(last_child)
				goal_reached = True
				return 'DONE'
			#check if child is not already in visited_nodes
			node_already_visited = False
			node_already_visited = child[0] in visited_nodes_states
			if not node_already_visited:
				#* child will be the latest element
				counter_nodes += 1
				generated_nodes.append((child[0],counter_nodes, child[2]))

def generate_path(node, goal_path):
	"""_summary_

	Args:
		node (Node): current node to evaluate its parent( previous move done)
		goal_path (array): Array of Node class instances where the first element is the goal state

	Returns:
		function: generate_path is called until initial node state is reached
	"""
	goal_path.append(node[0])
	if node[2] is None:
		return
	return generate_path(visited_nodes[node[2]], goal_path)

def store_nodes():
	"""Stores all the nodes generated with the function @create_nodes
	"""
	file_nodes = open("Nodes.txt", "w")
	for node in visited_nodes:
		node_sequence = " ".join(to_string_sequence(node[0]))
		file_nodes.write(f'{ node_sequence }\n')
	file_nodes.close()
	return
def store_node_path():
	"""Stores the actions in order which solves the puzzle for the initial and goal state given by the user.
	"""
	file_nodes_path = open("nodePath.txt", "w")
	for node in goal_path[::-1]:
		node_sequence = " ".join(to_string_sequence(node))
		file_nodes_path.write(f'{ node_sequence }\n')
	file_nodes_path.close()
	return
def store_nodes_info():
	"""Stores complete info of every Node in the State space generated
	"""
	file_nodes_info = open("NodesInfo.txt", "w")
	file_nodes_info.write('Node_index   Parent_Node_index	Node\n')
	for node in visited_nodes:
		node_sequence = " ".join(to_string_sequence(node[0]))
		node_parent = node[2] if node[2] else 0
		file_nodes_info.write(f'{ node[1] }	{ node_parent }	{ node_sequence }\n')
	file_nodes_info.close()
	return

#User Input Initial and goal state
print('Welcome to 8 puzzle game solver!')
initial_state = input_matrix('INITIAL')
goal_state = input_matrix('GOAL')

#Initialize main variables
generated_nodes = deque([]) #open list for BSF
visited_nodes = [] #closed list for BSF
visited_nodes_states = set([]) #To check if node is already visited or not
goal_path = [] #for backtracking

#Using Breadth First Search to generate the State space
print(create_nodes(initial_state, goal_state))
#Strategy to find the solution of the puzzle
generate_path(visited_nodes[-1], goal_path)
# Save the information for simulate the solution
store_nodes()
store_node_path()
store_nodes_info()