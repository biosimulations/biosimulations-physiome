/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 *
 * The contents of this file are subject to the Mozilla Public License Version
 * 1.1 (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 *
 * Software distributed under the License is distributed on an "AS IS" basis,
 * WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
 * for the specific language governing rights and limitations under the
 * License.
 *
 * The Original Code is "Andre's Reference Description Framework".
 *
 * The Initial Developer of the Original Code is
 * David Nickerson <nickerso@users.sourceforge.net>.
 * Portions created by the Initial Developer are Copyright (C) 2007-2008
 * the Initial Developer. All Rights Reserved.
 *
 * Contributor(s):
 *
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 *
 * ***** END LICENSE BLOCK ***** */
/*
  Define a class to handle modification metadata
*/
dojo.provide("andre.ModificationData");
dojo.require("andre.Person");
dojo.require("andre.Date");
dojo.require("andre.utils");
dojo.declare("andre.ModificationData", null, {
  store: null,
  items: null,
  /* constructor simply saves the items and its store so that data can be fetched
     out as required */
  constructor: function(store, items) {
    this.store = store;
    this.items = items;
  },
  /* create a dom node suitable for appending to an XHTML document */
  // FIXME: deprecated in favour of toNode() and toNodeShort()
  toDOMNode: function() {
    // make sure our items are still in the store ???
    dojo.forEach(this.items,function(item,index,items) {
      if (!this.store.isItem(item)) {
        console.debug("Modification item no longer in store?");
        return null;
      }
    });
    // sort items most recent -> oldest modification
    this.sortItems();
    // use the id of the most recent modification
    var id = this.store.getIdentity(this.items[0]);
    // create the main element for this data
    var element = dojo.doc.createElement("div");
    dojo.addClass(element,"modification-container");
    element.setAttribute("id",id + "-container");
    // make the text anchor from the most recent modification
    var p = new andre.Person(this.store,this.store.getValue(this.items[0],"modifier"));
    var d = new andre.Date(this.store.getValue(this.items[0],"modified"));
    var anchorString = "Last modified: " + d.shortString() + ", " + p.shortString();
    // and assemble the full content of the modification display
    // FIXME: could maybe look at the dojo grid for this?
    var content = dojo.doc.createElement("div");
    dojo.style(content,"overflow","auto");
    var table = content.appendChild(dojo.doc.createElement("table"));
    dojo.addClass(table,"modification-table");
    var thead = table.appendChild(dojo.doc.createElement("thead"));
    var row = thead.appendChild(dojo.doc.createElement("tr"));
    var td = row.appendChild(dojo.doc.createElement("th"));
    td.innerHTML = "Date";
    dojo.style(td,"width","20%");
    td = row.appendChild(dojo.doc.createElement("th"));
    td.innerHTML = "Modification";
    dojo.style(td,"width","50%");
    row.appendChild(dojo.doc.createElement("th")).innerHTML = "Modifier";
    var oddRow = true;
    var tbody = table.appendChild(dojo.doc.createElement("tbody"));
    dojo.forEach(this.items,function(item,index,items) {
      p = new andre.Person(this.store,this.store.getValue(item,"modifier"));
      d = new andre.Date(this.store.getValue(item,"modified"));
      var desc = this.store.getValue(item,"modification");
      row = tbody.appendChild(dojo.doc.createElement("tr"));
      if (oddRow) { dojo.addClass(row,"odd-row"); }
      row.appendChild(dojo.doc.createElement("td")).innerHTML = d.fullString();
      row.appendChild(dojo.doc.createElement("td")).innerHTML = desc;
      row.appendChild(dojo.doc.createElement("td")).innerHTML = p.fullString();
      oddRow = !oddRow;
    });
    // and make the anchored data display
    var expItem =  andre.utils.createAnchoredExpandingItem(id,anchorString,content);
    element.appendChild(expItem);
    return element;
  },
  /* create a simple string containing a short description of this modification data */
  toStringShort: function() {
    // make sure our items are still in the store ???
    dojo.forEach(this.items,function(item,index,items) {
      if (!this.store.isItem(item)) {
        console.debug("Modification item no longer in store?");
        return "";
      }
    });
    // sort items most recent -> oldest modification
    this.sortItems();
    var p = new andre.Person(this.store,this.store.getValue(this.items[0],"modifier"));
    var d = new andre.Date(this.store.getValue(this.items[0],"modified"));
    var anchorString = "Last modified: " + d.shortString() + ", " + p.shortString();
    return anchorString;
  },
  /* create a single DOM node containing a short description of this modification data */
  toNodeShort: function() {
    var anchorString = this.toStringShort();
    if (anchorString != "") {
      var element = dojo.doc.createElement("span");
      dojo.addClass(element,"short-modification-container");
      // make the text anchor from the most recent modification
      element.innerHTML = anchorString;
      return element;
    } else {
      return null;
    }
  },
  /* create a single DOM node containing a complete display of this modification data */
  toNode: function() {
    // make sure our items are still in the store ???
    dojo.forEach(this.items,function(item,index,items) {
      if (!this.store.isItem(item)) {
        console.debug("Modification item no longer in store?");
        return null;
      }
    });
    // sort items most recent -> oldest modification
    this.sortItems();
    // create the main element for this data
    var element = dojo.doc.createElement("div");
    dojo.addClass(element,"modification-container");
    // assemble the full content of the modification display
    // FIXME: could maybe look at the dojo grid for this?
    var table = element.appendChild(dojo.doc.createElement("table"));
    dojo.addClass(table,"modification-table");
    var thead = table.appendChild(dojo.doc.createElement("thead"));
    var row = thead.appendChild(dojo.doc.createElement("tr"));
    var td = row.appendChild(dojo.doc.createElement("th"));
    td.innerHTML = "Date";
    dojo.style(td,"width","20%");
    td = row.appendChild(dojo.doc.createElement("th"));
    td.innerHTML = "Modification";
    dojo.style(td,"width","50%");
    row.appendChild(dojo.doc.createElement("th")).innerHTML = "Modifier";
    var oddRow = true;
    var tbody = table.appendChild(dojo.doc.createElement("tbody"));
    dojo.forEach(this.items,function(item,index,items) {
      var p = new andre.Person(this.store,this.store.getValue(item,"modifier"));
      var d = new andre.Date(this.store.getValue(item,"modified"));
      var desc = this.store.getValue(item,"modification");
      row = tbody.appendChild(dojo.doc.createElement("tr"));
      if (oddRow) dojo.addClass(row,"odd-row");
      row.appendChild(dojo.doc.createElement("td")).innerHTML = d.fullString();
      row.appendChild(dojo.doc.createElement("td")).innerHTML = desc;
      row.appendChild(dojo.doc.createElement("td")).innerHTML = p.fullString();
      oddRow = !oddRow;
    });
    return element;
  },
  sortItems: function() {
    // sort items in the list so most recent is first and oldest last
    this.items.sort(function(a,b) {
      var aTime = this.store.getValue(a,"modified");
      var bTime = this.store.getValue(b,"modified");
      return (bTime - aTime);
    });
  }
});
