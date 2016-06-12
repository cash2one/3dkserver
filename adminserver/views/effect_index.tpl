<div class="ui-state-active"><h3><b>特效数值管理</b></h3></div>
<div style="margin:0px 0px 30px 0px;">
<div style="padding:5px 10px;height:50px;border:0px;" class="ui-widget-header">
    <div style="float:left;">
    <button id="export" onclick="$(location).attr('href', '/effect/export');return false;"><span class="ui-icon ui-icon-circle-arrow-s"></span>全表导出</button>
    </div>
    <div style="float:left;margin-left:20px;">
    <form id="upload" action="/effect/import" method="POST" enctype="multipart/form-data">
    <input type="file" name="data" id="csv"/>
    <button id="import"><span class="ui-icon ui-icon-circle-arrow-n"></span>全表导入</button>
    <button id="recover" onclick="$(location).attr('href', '/effect/recover');return false;"><span class="ui-icon ui-icon-circle-arrow-n"></span>恢复</button>
    </form>
    </div>
</div>
<table id="data" class="display dataTable" width="100%" cellspacing="0" cellpadding="0" border="0" style="width:
100%;text-align:center;">
<thead>
    <tr>
        <th>#</th>
        <th>特效类型</th>
        <th>起手特效</th>
        <th>起手特效延迟时间</th>
        <th>起手特效时长</th>
        <th>技能起手音效</th>
        <th>飞行特效</th>
        <th>飞行特效延迟时间</th>
        <th>飞行特效时长</th>
        <th>飞行音效</th>
        <th>受击特效</th>
        <th>受击特效延迟时间</th>
        <th>受击特效时长</th>
        <th>技能命中音效</th>
        <th>操作</th>
    </tr>
</thead>
<tbody>
%for row in data:
<tr class="gradeA">
    <td>{{row[0]}}</td>
    <td>{{row[1]}}</td>
    <td>{{row[2]}}</td>
    <td>{{row[3]}}</td>
    <td>{{row[4]}}</td>
    <td>{{row[5]}}</td>
    <td>{{row[6]}}</td>
    <td>{{row[7]}}</td>
    <td>{{row[8]}}</td>
    <td>{{row[9]}}</td>
    <td>{{row[10]}}</td>
    <td>{{row[11]}}</td>
    <td>{{row[12]}}</td>
    <td>{{row[13]}}</td>
    <td style="width:60px;">
        <button id="delete" style="width:20px;height:20px;" onclick="return effect_delete({{row[0]}}, {{row[1]}});"></button>
    </td>
</tr>
%end
</tbody>
</table>
</div>
<div style="height:500px;"></div>
%rebase content_base js='effect'
