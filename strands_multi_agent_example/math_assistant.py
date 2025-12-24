from __future__ import annotations

from strands import tool
import sympy as sp
import re


def normalize_expression(expr: str) -> str:
    """
    Convert implicit multiplication to explicit:
    5x  -> 5*x
    2(x+1) -> 2*(x+1)
    x(x+1) -> x*(x+1)
    """
    expr = expr.replace("−", "-").replace("^", "**")

    # number followed by variable: 5x -> 5*x
    expr = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", expr)

    # variable followed by number: x2 -> x*2
    expr = re.sub(r"([a-zA-Z])(\d)", r"\1*\2", expr)

    # variable followed by '(' : x( -> x*(
    expr = re.sub(r"([a-zA-Z])\(", r"\1*(", expr)

    # ')' followed by variable or number: )( -> )*( , )x -> )*x
    expr = re.sub(r"\)([a-zA-Z0-9])", r")*\1", expr)

    return expr


@tool
def math_assistant(query: str) -> str:
    """
    Deterministic math solver using SymPy.
    No Bedrock tool calling. Safe for workshop demos.
    """
    print("Routed to Math Assistant")

    try:
        q = query.lower().strip()

        # Remove common leading phrases
        for prefix in [
            "solve the quadratic equation",
            "solve quadratic equation",
            "solve the equation",
            "solve equation",
            "solve",
        ]:
            if q.startswith(prefix):
                q = q[len(prefix):].strip()

        # Split equation
        if "=" in q:
            lhs, rhs = q.split("=", 1)
        else:
            lhs, rhs = q, "0"

        lhs = normalize_expression(lhs)
        rhs = normalize_expression(rhs)

        x = sp.Symbol("x")
        lhs_expr = sp.sympify(lhs)
        rhs_expr = sp.sympify(rhs)

        eq = sp.Eq(lhs_expr, rhs_expr)
        solutions = sp.solve(eq, x)

        if not solutions:
            return "No solutions found."

        sol_str = ", ".join(str(s) for s in solutions)

        checks = []
        for s in solutions:
            val = sp.simplify(lhs_expr.subs(x, s) - rhs_expr)
            checks.append(f"Check at x={s}: {val}")

        return (
            f"Solutions: x = {sol_str}\n\n"
            "Verification:\n- " + "\n- ".join(checks)
        )

    except Exception as e:
        return (
            "I can solve algebraic equations, but couldn’t parse this one.\n\n"
            f"Error: {str(e)}\n\n"
            "Try formats like:\n"
            "- x^2 + 5x + 6 = 0\n"
            "- x**2 + 5*x + 6 = 0"
        )
