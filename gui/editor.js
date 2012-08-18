function EditorConstructor ()
{
    this.load_symbol = function (new_symbol)
    {
        commit_symbol();
        if (new_symbol === null) {
            document.getElementById("editor_field").value = "";
        } else if (new_symbol in symbol_values) {
            document.getElementById("editor_field").value =
                symbol_values[new_symbol];

            dom_editor_symlist = document.getElementById("editor_symlist");
            var ret = search_select_value(dom_editor_symlist, new_symbol);
            if (ret == null)
                return false;

            dom_editor_symlist.selectedIndex = ret[0];
        } else {
            return false;
        }
        current_symbol = new_symbol;
        return true;
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
        var ret = search_select_value(dom_editor_symlist, old_symbol);
        if (ret == null)
            return false;
        dom_editor_symlist.removeChild(ret[1]);

        var v = dom_editor_symlist.value;
        this.load_symbol((v === "") ? null : v);
        return true;
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
            symbol_values[current_symbol] =
                document.getElementById("editor_field").value;
    };

    function search_select_value (select_obj, target)
    {
        for (var i = 0; i < select_obj.length; i++) {
            var option_obj = select_obj[i];
            if (option_obj.value === target)
                return [i, option_obj];
        }
        return null;
    };

    var current_symbol = null;
    var symbol_values = new Object();
}

var editor = new EditorConstructor();
