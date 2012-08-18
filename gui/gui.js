function init ()
{
    /* nested helper function */
    function listeners_helper (col_t_string)
    {
        var col_t = col_expand_manager.COL_T[col_t_string];
        return {
            "onclick": function ()
            {
                col_expand_manager.toggle_expand(col_t);
            },

            "onload": function ()
            {
                col_expand_manager.register(col_t, this);
            },
        };
    }

    var listeners = {
        "console_expand": listeners_helper("CONSOLE"),
        "editor_expand": listeners_helper("EDITOR"),
        "docs_expand": listeners_helper("DOCS"),
        "editor_symlist":
        {
            "onchange": function ()
            {
                editor.load_symbol(this.value);
            },
        },

        "editor_newsym":
        {
            "onclick": function ()
            {
                var new_symbol = prompt("New symbol name:")
                if (new_symbol == null || new_symbol.length <= 0)
                    return;
                editor.add_symbol(new_symbol);
                editor.load_symbol(new_symbol);
            },
        },

        "editor_delsym":
        {
            "onclick": function ()
            {
                editor.del_symbol(editor.current_symbol());
            },
        },
    };

    register_event_listeners(listeners);
}

function register_event_listeners (listeners)
{
    for (var dom_id in listeners) {
        for (var event_id in listeners[dom_id]) {
            var listener = listeners[dom_id][event_id];
            document.getElementById(dom_id)[event_id] = listener;
            if (event_id == "onload") {
                document.getElementById(dom_id)[event_id]();
            }
        }
    }
}

function ColExpandManager ()
{
    this.register = function (col_t, dom_obj)
    {
        dom_registry[col_t] = dom_obj;
    };

    this.toggle_expand = function (col_t)
    {
        if (col_t === expanded_column) {
            unexpand(this);
            expanded_column = null;
        } else {
            expand(this, col_t);
            expanded_column = col_t;
        }
    };

    function expand (self, col_t)
    {
        for (var sub_col_t in SYMBOLS) {
            var is_expanded_col_t = (sub_col_t === col_t) ? 1 : 0;
            var symbol = SYMBOLS[sub_col_t][is_expanded_col_t]
            dom_registry[sub_col_t].setAttribute("value", symbol);
        }

        for (var sub_col_t in COL_WIDTHS[col_t]) {
            var dom_obj = dom_registry[sub_col_t].parentElement.parentElement;
            var width = COL_WIDTHS[col_t][sub_col_t];
            dom_obj.style.width = width;
        }
    }

    function unexpand (self)
    {
        for (var col_t in SYMBOLS) {
            dom_registry[col_t].setAttribute("value", SYMBOLS[col_t][0]);
            dom_registry[col_t].parentElement.parentElement.style.width = "";
        }
    }

    this.COL_T = {
        "CONSOLE" : "0",
        "EDITOR" : "1",
        "DOCS" : "2",
    };

    var SYMBOLS = new Object();
    SYMBOLS[this.COL_T.CONSOLE] = [">", "<"];
    SYMBOLS[this.COL_T.EDITOR] = [">", "<"];
    SYMBOLS[this.COL_T.DOCS] = ["<", ">"];

    var COL_WIDTHS = new Object();
    COL_WIDTHS[this.COL_T.CONSOLE] = new Object();
    COL_WIDTHS[this.COL_T.CONSOLE][this.COL_T.CONSOLE] = "59%";
    COL_WIDTHS[this.COL_T.CONSOLE][this.COL_T.EDITOR] = "9%";
    COL_WIDTHS[this.COL_T.CONSOLE][this.COL_T.DOCS] = "";

    COL_WIDTHS[this.COL_T.EDITOR] = new Object();
    COL_WIDTHS[this.COL_T.EDITOR][this.COL_T.CONSOLE] = "";
    COL_WIDTHS[this.COL_T.EDITOR][this.COL_T.EDITOR] = "59%";
    COL_WIDTHS[this.COL_T.EDITOR][this.COL_T.DOCS] = "4%";

    COL_WIDTHS[this.COL_T.DOCS] = new Object();
    COL_WIDTHS[this.COL_T.DOCS][this.COL_T.CONSOLE] = "";
    COL_WIDTHS[this.COL_T.DOCS][this.COL_T.EDITOR] = "9%";
    COL_WIDTHS[this.COL_T.DOCS][this.COL_T.DOCS] = "54%";

    var expanded_column = null;
    var dom_registry = new Object();
}

var col_expand_manager = new ColExpandManager();
