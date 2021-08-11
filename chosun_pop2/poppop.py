hat_txt = """<!DOCTYPE html>
<html> <!-- Demo version Completed HERE! OK.-->
    <head>
        <meta charset = "utf-8">
        <style type = "text/css">
            table{
                border-collapse: collapse;
                border: 2px solid black}
            th{
                border: 1px solid black}
            td{
                border: 1px solid black}
            tr.red{
              background-color: #9cc069;
            }
            div{
                width: 100%}
            div.left{
                padding-left: 10px;
                padding-right: 1000px;
                float: left;}
            div.right{
                position: fixed;
                overflow: scroll;
                width: 150px;
                height: 750px;
                right: 50px;;
                display: inline-block;
                background-color: white;
                padding: 5px;}
            div.show-result{
                font-size: larger;
                color: white;
                background-color: royalblue;}
            hr.rge-separate{
                border: solid 1px black;
                width: 80%;}
        </style>
    </head>
    <body>
    <h1 style = "padding-left: 10px"> 안녕? </h1>
    <div onclick = "pooling()">"""

tail_txt = '''<div class='right' name = "divright" onclick = "open_it()">
        <div class = "show-result"> <strong>YES SAME</strong> </div>
        <div id = "same_pool"></div><p>
        <hr><p>
        <div class = "show-result"> <strong>No, DIFF</strong> </div>
        <div id = "diff_pool"></div><p>
        <hr><p>
        <hr><p><br/><p/>
        <input type = "button" value = "open it" class = "click-button" onclick = "open_it()"> &nbsp; &nbsp; &nbsp;
        <input type = "button" onclick = "download_it()" value = "download it" class = "click-button"> <p/>
    </div>
        <script = "text/javascript">

            var all_idx_bySets = new Array();
            var forms = document.getElementsByName("form");
            for (var f = 0; f < forms.length; f++){
                var form = forms[f]
                var form_tbs = form.getElementsByTagName("table")
                //
                var idx_bySets = new Array();
                for (var i = 0; i < form_tbs.length; i++){
                    var elem = form_tbs[i];
                    var idx_nb = elem.id.replace("table_idx", "");
                    idx_bySets.push(idx_nb)}//
                all_idx_bySets.push(idx_bySets)}//

            function pooling(){
                var same_pool = new Array();
                var diff_pool = new Array();
                for (var r = 0; r < all_idx_bySets.length; r++){
                    var idx_byS = all_idx_bySets[r]
                    var idx0 = idx_byS[0]
                    var idx1 = idx_byS[1]

                    var elem_same = document.getElementById("same_id" + idx0  + "_" + idx1)
                    var elem_diff = document.getElementById("diff_id" + idx0  + "_" + idx1)

                    if (elem_same.checked == true){same_pool.push(idx0 + "_" + idx1)};
                    if (elem_diff.checked == true){diff_pool.push(idx0 + "_" + idx1)}}

                // show the result lists.
                document.getElementById("same_pool").innerHTML = same_pool
                document.getElementById("diff_pool").innerHTML = diff_pool
                //
                }

    </script>
    </body>
</html>'''


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


def return_table_on_html(df, cp_list):
    import time

    kt_abs = []

    for cii, cp in enumerate(cp_list):
        if cii%10 == 5:
            time.sleep(0.5)

        a, b = cp[0], cp[1]
        a_hh, b_hh = hh_uni_idx[a], hh_uni_idx[b]

        a_hh_offset = a_hh.index(a)
        b_hh_offset = b_hh.index(b)

        tt_a = df[df.index.isin(a_hh)].copy().reset_index().drop(['index'], axis=1)
        tt_a = pd.concat([pd.DataFrame({"index": a_hh}), tt_a], axis=1)
        tt_a_html = tt_a.to_html(index=False)

        time.sleep(0.5)

        tt_b = df[df.index.isin(b_hh)].copy().reset_index().drop(['index'], axis=1)
        tt_b = pd.concat([pd.DataFrame({"index": b_hh}), tt_b], axis=1)
        tt_b_html = tt_b.to_html(index=False)

        spt_a = tt_a_html.split("<tr>")
        k = "<tr>".join(spt_a[:a_hh_offset+1])
        t = "<tr>".join(spt_a[a_hh_offset+1:])
        kt_a = k + "<tr class='red'>" + t
        kt_a = kt_a.replace("\n", "")
        kt_a = kt_a.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" id="table_idx{}" name="table1"'.format(a))

        spt_b = tt_b_html.split("<tr>")
        k = "<tr>".join(spt_b[:b_hh_offset+1])
        t = "<tr>".join(spt_b[b_hh_offset+1:])
        kt_b = k + "<tr class='red'>" + t
        kt_b = kt_b.replace("\n", "")
        kt_b = kt_b.replace('<table border="1" class="dataframe">', '<table border="1" class="dataframe" id="table_idx{}" name="table2"'.format(b))

        kt_ab = "<p>(" + str(a) + ", " + str(b) + "),</p>" + '\n<form name = "form">\n' + kt_a + "\n <br/> \n" + kt_b + '\n</form>\n'
        
        time.sleep(0.5)

        input_TXT = f'<div> &nbsp; &nbsp; &nbsp; same? <input type = "checkbox" class = "same" id = "same_id{a}_{b}" value = "same?"> </input> &nbsp; &nbsp; &nbsp; diff? <input type = "checkbox" class = "same" id = "diff_id{a}_{b}" value = "diff?"> </input> </div>'

        kt_ab = kt_ab + input_TXT + '\n<br/>\n<hr align = "left" class = "rge-separate">'
        kt_ab = "<div class='left'>\n" + kt_ab + '</div>'

        kt_abs.append(kt_ab)

    time.sleep(0.5)

    kt_abs = "\n\n".join(kt_abs)

    kt_abs = hat_txt + "\n\n" + kt_abs + "\n\n" + tail_txt

    return kt_abs


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #