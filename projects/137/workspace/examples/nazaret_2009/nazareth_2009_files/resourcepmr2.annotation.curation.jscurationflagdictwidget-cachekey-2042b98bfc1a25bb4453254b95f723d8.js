
/* - ++resource++pmr2.annotation.curation.js/curationflagdictwidget.js - */
// http://models.cellml.org/portal_javascripts/++resource++pmr2.annotation.curation.js/curationflagdictwidget.js?original=1
CurationFlagDictCounter=new function f(){this.counter=0;this.next=function(){result=this.counter;this.counter=this.counter+1;return result}}
function appendWidgetRow(selector,widgetName,key,value){var i=CurationFlagDictCounter.next()
var editor=jq(selector);var rowid=widgetName+'-row'+i
editor.append('<tr id="'+rowid+'">'+'<td>'+'<input type="text" name="'+widgetName+'-key'+i+'" value="'+key+'"/>'+'</td>'+'<td>'+'<input type="text" name="'+widgetName+'-value'+i+'" value="'+value+'"/>'+'</td>'+'<td>'+'<button type="button" value="delete" '+'onclick="javascript:deleteWidgetRow(\''+selector+' > #'+rowid+'\')">delete</button>'+'</td>'+'</tr>'+'');return i}
function deleteWidgetRow(rowid){jq(rowid).remove()}
function appendNewWidgetRow(selector,widgetName){row=appendWidgetRow(selector,widgetName,'','');jq(selector+' [name='+widgetName+'-key'+row+']').select()}
function calcCurationFlagDictWidget(widgetId){var widgetName='curationflagdict';var divId='#'+widgetName+'-'+widgetId;var selector=divId+'-anchor';var inputs=jq(selector+' input');results='';for(var i=0;i<inputs.length;i++){results=results+inputs[i].value+'\n'}
jq('#'+widgetId).val(results)}
function appendCurationFlagDictWidget(widgetId){var widgetName='curationflagdict';var divId='#'+widgetName+'-'+widgetId;var selector=divId+'-anchor';var curationDiv=jq(divId);curationDiv.after('<table></table>');curationDiv.css('display','none');var textareaId='#'+widgetId;var values=jq(textareaId).val().split('\n');values.reverse();var structure=jq(divId+' + table');structure.append('<thead><tr><th>Flag Values</th>'+'<th>Description</th></tr></thead>');structure.append('<tbody id="'+selector.substr(1)+'"></tbody>');while(values.length){key=values.pop();value=values.pop()||'';if(key){appendWidgetRow(selector,widgetName,key,value)}}
structure.append('<tfoot><tr><th colspan="2"><button type="button" value="New Flag Value"'+' onclick="javascript:appendNewWidgetRow(\''+selector+'\', \''+widgetName+'\')">New Flag Value</button></th></tr>');jq(textareaId).parents('form').bind('submit', function f(){calcCurationFlagDictWidget(widgetId)})}

