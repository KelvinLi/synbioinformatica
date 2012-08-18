function EditorConstructor ()
{
    this.load_symbol = function (new_symbol)
    {
        commit_symbol();
        if (!(new_symbol in symbol_values))
            return false;

        document.getElementById("editor_field").value = symbol_values[new_symbol];

        for (var i = 0; i < document.getElementById("editor_symlist").length; i++) {
            if (document.getElementById("editor_symlist")[i].value === new_symbol) {
                document.getElementById("editor_symlist").selectedIndex = i;
                current_symbol = new_symbol;
                return true;
            }
        }
        return false;
    };

    this.add_symbol = function (new_symbol)
    {
        if (new_symbol in symbol_values)
            return false;

        symbol_values[new_symbol] = "";

        var new_dom_obj = document.createElement("option");
        new_dom_obj.setAttribute("value", new_symbol);
        new_dom_obj.appendChild(document.createTextNode(new_symbol));
        document.getElementById("editor_symlist").appendChild(new_dom_obj);
        return true;
    };

    this.del_symbol = function (old_symbol)
    {
        if (!(old_symbol in symbol_values))
            return false;

        delete symbol_values[old_symbol];
        
        var dom_editor_symlist = document.getElementById("editor_symlist");
        for (var i = 0; i < dom_editor_symlist.length; i++) {
            var child = dom_editor_symlist[i];
            if (child.value === old_symbol) {
                dom_editor_symlist.removeChild(child);

                if (dom_editor_symlist.value == null ||
                    dom_editor_symlist.value === "")
                    document.getElementById("editor_field").value = "";
                else
                    this.load_symbol(dom_editor_symlist.value);

                return true;
            }
        }
        return false;
    };

    this.symbols = function ()
    {
        return Object.keys(symbol_values);
    };

    this.current_symbol = function ()
    {
        return current_symbol;
    };

    function commit_symbol ()
    {
        if (current_symbol in symbol_values)
            symbol_values[current_symbol] = document.getElementById("editor_field").value;
    };

    var current_symbol = null;
    var symbol_values = new Object();
}

var editor = new EditorConstructor();
