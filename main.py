import tkinter as tk
import ast
import operator as _op


def safe_eval(expr: str):
	"""Safely evaluate a math expression using AST (supports + - * / % ** and unary ops)."""
	operators = {
		ast.Add: _op.add,
		ast.Sub: _op.sub,
		ast.Mult: _op.mul,
		ast.Div: _op.truediv,
		ast.Mod: _op.mod,
		ast.Pow: _op.pow,
	}

	def _eval(node):
		if isinstance(node, ast.BinOp):
			left = _eval(node.left)
			right = _eval(node.right)
			op_type = type(node.op)
			if op_type in operators:
				return operators[op_type](left, right)
			raise ValueError("Unsupported operator")
		if isinstance(node, ast.UnaryOp):
			if isinstance(node.op, ast.UAdd):
				return +_eval(node.operand)
			if isinstance(node.op, ast.USub):
				return -_eval(node.operand)
			raise ValueError("Unsupported unary operator")
		if isinstance(node, ast.Num):
			return node.n
		if isinstance(node, ast.Constant):
			if isinstance(node.value, (int, float)):
				return node.value
			raise ValueError("Unsupported constant type")
		raise ValueError("Unsupported expression")

	parsed = ast.parse(expr, mode="eval")
	return _eval(parsed.body)


class Calculator(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Calculator")
		self.resizable(False, False)
		self._create_widgets()

	def _create_widgets(self):
		self.display_var = tk.StringVar()
		entry = tk.Entry(self, textvariable=self.display_var, font=("Segoe UI", 20), bd=5, relief=tk.RIDGE, justify='right')
		entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
		entry.focus_set()

		btn_text = [
			('7', '8', '9', '/'),
			('4', '5', '6', '*'),
			('1', '2', '3', '-'),
			('0', '.', '=', '+'),
		]

		for r, row in enumerate(btn_text, start=1):
			for c, ch in enumerate(row):
				action = (lambda x=ch: self._on_button(x))
				b = tk.Button(self, text=ch, width=4, height=2, font=("Segoe UI", 16), command=action)
				b.grid(row=r, column=c, sticky="nsew", padx=3, pady=3)

		tk.Button(self, text='C', width=4, height=2, font=("Segoe UI", 16), command=self.clear).grid(row=5, column=0, padx=3, pady=3)
		tk.Button(self, text='←', width=4, height=2, font=("Segoe UI", 16), command=self.backspace).grid(row=5, column=1, padx=3, pady=3)
		tk.Button(self, text='(', width=4, height=2, font=("Segoe UI", 16), command=lambda: self._on_button('(')).grid(row=5, column=2, padx=3, pady=3)
		tk.Button(self, text=')', width=4, height=2, font=("Segoe UI", 16), command=lambda: self._on_button(')')).grid(row=5, column=3, padx=3, pady=3)

		self.bind('<Return>', lambda e: self._on_button('='))
		self.bind('<BackSpace>', lambda e: self.backspace())

	def _on_button(self, char):
		if char == '=':
			self.calculate()
			return
		current = self.display_var.get()
		self.display_var.set(current + char)

	def clear(self):
		self.display_var.set('')

	def backspace(self):
		self.display_var.set(self.display_var.get()[:-1])

	def calculate(self):
		expr = self.display_var.get().strip()
		if not expr:
			return
		try:
			result = safe_eval(expr)
			# Format result: drop .0 for integers
			if isinstance(result, float) and result.is_integer():
				result = int(result)
			self.display_var.set(str(result))
		except Exception:
			self.display_var.set('Error')


if __name__ == '__main__':
	app = Calculator()
	app.mainloop()

