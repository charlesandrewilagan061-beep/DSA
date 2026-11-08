import math

from flask import Flask, render_template, request, redirect, url_for, flash

from linked_list import LinkedList
from infix_postfix import infix_to_postfix
from queuedequeue import Queue
from sorting import sort_numbers, ALGORITHMS, DESCRIPTIONS
from binarytree import BinaryTree

app = Flask(__name__)
app.secret_key = 'change-this-secret-key'  # needed for flash() messages

# HTTP is stateless, so the list lives here at module level and survives
# between requests for as long as the server keeps running.
my_list = LinkedList()
my_queue = Queue()
my_tree = BinaryTree()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/works/uppercase', methods=['GET', 'POST'])
def uppercase():
    result = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()   
    return render_template('touppercase.html', result=result)

@app.route('/works/area/circle', methods=['GET', 'POST'])
def acircle():
    result = None
    error = None
    if request.method == 'POST':
        try:
            radius = float(request.form.get('radius', ''))
            if radius < 0:
                raise ValueError
            result = round(math.pi * radius ** 2, 4)
        except ValueError:
            error = 'Please enter a valid non-negative number for the radius.'
    return render_template('circle.html', result=result, error=error)

# @app.route('/areaOfcirle', methods=['GET', 'POST'])
# def areaOfcirle():
#     result = None
#     name=request.get('name','')
#     print(name)
#     if request.method == 'POST':
#         input_string = request.form.get('inputradius', '')
#         result = int(input_string) * int(input_string) * 3.14
#     return render_template('areaCircle.html', result=result)

@app.route('/works/area/triangle', methods=['GET', 'POST'])
def atriangle():
    result = None
    error = None
    if request.method == 'POST':
        try:
            base = float(request.form.get('base', ''))
            height = float(request.form.get('height', ''))
            if base < 0 or height < 0:
                raise ValueError
            result = round(0.5 * base * height, 4)
        except ValueError:
            error = 'Please enter valid non-negative numbers for the base and height.'
    return render_template('triangle.html', result=result, error=error)

@app.route('/works/linkedlist', methods=['GET', 'POST'])
def linkedlist():
    search_result = None
    if request.method == 'POST':
        action = request.form.get('action', '')
        value = request.form.get('value', '').strip()
        index_text = request.form.get('index', '').strip()

        try:
            if action in ('insert_head', 'insert_tail', 'insert_index', 'delete_value', 'search') and value == '':
                raise ValueError('Please enter a value.')

            if action == 'insert_head':
                my_list.insert_at_head(value)
                flash(f'Inserted "{value}" at the head.', 'success')
            elif action == 'insert_tail':
                my_list.insert_at_tail(value)
                flash(f'Inserted "{value}" at the tail.', 'success')
            elif action == 'insert_index':
                my_list.insert_at_index(int(index_text), value)
                flash(f'Inserted "{value}" at index {int(index_text)}.', 'success')
            elif action == 'delete_head':
                flash(f'Deleted "{my_list.delete_head()}" from the head.', 'success')
            elif action == 'delete_tail':
                flash(f'Deleted "{my_list.delete_tail()}" from the tail.', 'success')
            elif action == 'delete_value':
                my_list.delete_value(value)
                flash(f'Deleted the first node with value "{value}".', 'success')
            elif action == 'delete_index':
                removed = my_list.delete_at_index(int(index_text))
                flash(f'Deleted "{removed}" at index {int(index_text)}.', 'success')
            elif action == 'search':
                position = my_list.search(value)
                if position == -1:
                    flash(f'"{value}" was not found in the list.', 'error')
                else:
                    flash(f'"{value}" found at index {position}.', 'success')
                    search_result = position
            elif action == 'reverse':
                my_list.reverse()
                flash('List reversed.', 'success')
            elif action == 'clear':
                my_list.clear()
                flash('List cleared.', 'success')
            else:
                flash('Unknown action.', 'error')
        except ValueError as e:
            message = str(e)
            if message.startswith('invalid literal for int()'):
                message = 'Please enter a whole number for the index.'
            flash(message, 'error')

        # Post/Redirect/Get: refreshing the page will not resubmit the form.
        return redirect(url_for('linkedlist', found=search_result))

    found = request.args.get('found', type=int)
    return render_template('linkedlist.html', items=my_list.to_list(), size=len(my_list), found=found)

@app.route('/works/infix-postfix', methods=['GET', 'POST'])
def infixpostfix():
    expression = ''
    result = None
    steps = None
    error = None
    if request.method == 'POST':
        expression = request.form.get('expression', '').strip()
        try:
            result, steps = infix_to_postfix(expression)
        except ValueError as e:
            error = str(e)
    return render_template('infixpostfix.html', expression=expression,
                           result=result, steps=steps, error=error)

@app.route('/works/queue', methods=['GET', 'POST'])
def queue_page():
    if request.method == 'POST':
        action = request.form.get('action', '')
        value = request.form.get('value', '').strip()

        if action == 'enqueue':
            if value:
                my_queue.enqueue(value)
                flash(f'Added "{value}" to the queue.', 'success')
            else:
                flash('Please enter a value.', 'error')

        elif action == 'dequeue':
            removed = my_queue.dequeue()

            if removed is None:
                flash('The queue is empty!', 'error')
            else:
                flash(f'Removed "{removed}" from the queue.', 'success')

        return redirect(url_for('queue_page'))

    return render_template(
        'queuedequeue.html',
        items=my_queue.to_list(),
        size=len(my_queue)
    )

@app.route('/works/binarytree', methods=['GET', 'POST'])
def binarytree():
    if request.method == 'POST':
        action = request.form.get('action', '')
        text = request.form.get('value', '').strip()
        found = None
        show_post = None

        try:
            if action in ('insert', 'search', 'delete') and text == '':
                raise ValueError('Please enter a number.')
            key = None
            if text != '':
                try:
                    number = float(text)
                except ValueError:
                    raise ValueError('Please enter a valid number.')
                key = int(number) if number.is_integer() else number

            if action == 'insert':
                my_tree.insert(key)
                flash(f'Inserted {key} into the tree.', 'success')
            elif action == 'search':
                if my_tree.search(my_tree.root, key) is None:
                    flash(f'{key} was not found in the tree.', 'error')
                else:
                    flash(f'{key} found. Path: ' + ' -> '.join(map(str, my_tree.search_path(key))), 'success')
                    found = key
            elif action == 'delete':
                my_tree.delete(key)
                flash(f'Deleted {key} from the tree.', 'success')
            elif action == 'postorder':
                if my_tree.root is None:
                    raise ValueError('The tree is empty.')
                show_post = 1
            elif action == 'clear':
                my_tree.clear()
                flash('Tree cleared.', 'success')
            else:
                flash('Unknown action.', 'error')
        except ValueError as e:
            flash(str(e), 'error')

        # Post/Redirect/Get: refreshing the page will not resubmit the form.
        return redirect(url_for('binarytree', found=found, post=show_post))

    found = request.args.get('found', type=float)
    if found is not None and found.is_integer():
        found = int(found)
    traversal = None
    if request.args.get('post'):
        traversal = my_tree.post_traversal(my_tree.root, '').rstrip('-').split('-')
    nodes, edges, depth = my_tree.layout()
    return render_template('binarytree.html', nodes=nodes, edges=edges, depth=depth,
                           size=len(my_tree), found=found, traversal=traversal)

@app.route('/works/sorting', methods=['GET', 'POST'])
def sorting():
    numbers = ''
    algorithm = 'bubble'
    frames = None
    error = None
    if request.method == 'POST':
        numbers = request.form.get('numbers', '').strip()
        algorithm = request.form.get('algorithm', 'bubble')
        try:
            result, frames = sort_numbers(numbers, algorithm)
        except ValueError as e:
            error = str(e)
    return render_template('sorting.html', numbers=numbers, algorithm=algorithm,
                           algorithms=ALGORITHMS, descriptions=DESCRIPTIONS,
                           frames=frames, error=error)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
