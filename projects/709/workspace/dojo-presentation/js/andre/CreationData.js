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
  Define a class to handle creation metadata
*/
dojo.provide("andre.CreationData");
dojo.require("andre.Person");
dojo.require("andre.Date");
dojo.require("andre.utils");
dojo.declare("andre.CreationData", null, {
  store: null,
  item: null,
  /* constructor simply saves the item and its store so that data can be fetched
     out as required */
  constructor: function(store, item) {
    this.store = store;
    this.item = item;
  },
  /* create a "brief" dom node suitable for appending to an XHTML document */
  // FIXME: deprecated in favour of toNode() and toNodeShort()
  toDOMNodeBrief: function() {
    // make sure our item is still in the store
    if (this.store.isItem(this.item)) {
      var id = this.store.getIdentity(this.item);
      // create the main element for this data
      var element = dojo.doc.createElement("span");
      dojo.addClass(element,"creation-brief-container");
      element.setAttribute("id",id + "-brief-container");
      // grab the creator
      var p = new andre.Person(this.store, this.store.getValue(this.item,"creator"));
      // and the created date
      var date = new andre.Date(this.store.getValue(this.item,"created"));
      // the string to use as the dialog anchor
      var anchorString = p.shortString() + " (" + date.shortString() + ")";
      element.appendChild(dojo.doc.createTextNode(anchorString));
      return element;
    } else {
      console.debug("The stored item is no longer in the data store?");
      return null;
    }
  },
  /* create a dom node suitable for appending to an XHTML document */
  // FIXME: deprecated in favour of toNode() and toNodeShort()
  toDOMNode: function() {
    // make sure our item is still in the store
    if (this.store.isItem(this.item)) {
      var id = this.store.getIdentity(this.item);
      // create the main element for this data
      var element = dojo.doc.createElement("div");
      dojo.addClass(element,"creation-container");
      element.setAttribute("id",id + "-container");
      // grab the creator
      var p = new andre.Person(this.store, this.store.getValue(this.item,"creator"));
      // and the created date
      var date = new andre.Date(this.store.getValue(this.item,"created"));
      // the string to use as the dialog anchor
      var anchorString = "Created: " + date.shortString() + ", " + p.shortString();
      // and the content of the dialog
      var dc = dojo.doc.createElement("div");
      dojo.style(dc,"overflow","auto");
      var dl = dc.appendChild(dojo.doc.createElement("dl"));
      dl.appendChild(dojo.doc.createElement("dt")).innerHTML = "Created:";
      dl.appendChild(dojo.doc.createElement("dd")).innerHTML = date.fullString();
      dl.appendChild(dojo.doc.createElement("dt")).innerHTML = "Creator:";
      dl.appendChild(dojo.doc.createElement("dd")).innerHTML = p.fullString();
      // and create the anchor and associated dialog
      var expItem = andre.utils.createAnchoredExpandingItem(id,anchorString,dc);
      element.appendChild(expItem);
      return element;
    } else {
      console.debug("The stored item is no longer in the data store?");
      return null;
    }
  },
  /* create a string containing a short display of this creation data */
  toStringShort: function() {
    // make sure our item is still in the store
    if (this.store.isItem(this.item)) {
      // grab the creator
      var p = new andre.Person(this.store, this.store.getValue(this.item,"creator"));
      // and the created date
      var date = new andre.Date(this.store.getValue(this.item,"created"));
      // the string to use as the short display
      var anchorString = "Created: " + date.shortString() + ", " + p.shortString();
      return anchorString;
    } else {
      console.debug("The stored item is no longer in the data store?");
      return "";
    }
  },
  /* create a single DOM node containing a short display of this creation data */
  toNodeShort: function() {
    var anchorString = this.toStringShort();
    if (anchorString != "") {
      // create the main element for this data
      var element = dojo.doc.createElement("span");
      dojo.addClass(element,"creation-container");
      element.innerHTML = anchorString;
      return element;
    } else {
      console.debug("The stored item is no longer in the data store?");
      return null;
    }
  },
  /* create a single DOM node containing the complete description of this creation data */
  toNode: function() {
    // make sure our item is still in the store
    if (this.store.isItem(this.item)) {
      // create the main element for this data
      var element = dojo.doc.createElement("div");
      dojo.addClass(element,"creation-container");
      // grab the creator
      var p = new andre.Person(this.store, this.store.getValue(this.item,"creator"));
      // and the created date
      var date = new andre.Date(this.store.getValue(this.item,"created"));
      // and the contents
      var dl = element.appendChild(dojo.doc.createElement("dl"));
      dl.appendChild(dojo.doc.createElement("dt")).innerHTML = "Created:";
      dl.appendChild(dojo.doc.createElement("dd")).innerHTML = date.fullString();
      dl.appendChild(dojo.doc.createElement("dt")).innerHTML = "Creator:";
      dl.appendChild(dojo.doc.createElement("dd")).innerHTML = p.fullString();
      return element;
    } else {
      console.debug("The stored item is no longer in the data store?");
      return null;
    }
  },
});
