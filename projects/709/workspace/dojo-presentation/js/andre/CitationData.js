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
  Define a class to handle citation metadata - need to ensure multiple citations
  are supported.
*/
dojo.provide("andre.CitationData");
dojo.require("andre.utils");
dojo.declare("andre.CitationData", null, {
  store: null,
  items: null,
  /* constructor simply saves the items and its store so that data can be fetched
     out as required */
  constructor: function(store, items) {
    this.store = store;
    this.items = items;
  },
  /* create a dom node suitable for appending to an XHTML document */
  // FIXME: deprecated in favour of toNodeShort and toNode
  toDOMNode: function() {
    // make sure our items are still in the store ???
    dojo.forEach(this.items,function(item,index,items) {
      if (!this.store.isItem(item)) {
        console.debug("Citation item no longer in store?");
        return null;
      }
    });
    // sort items 
    this.sortItems();
    // use the id of the most recent modification
    var id = this.store.getIdentity(this.items[0]);
    // create the main element for this data
    var element = dojo.doc.createElement("div");
    dojo.addClass(element,"citation-container");
    element.setAttribute("id",id + "-container");
    // and the content element for the display 
    var content = dojo.doc.createElement("div");
    dojo.style(content,"overflow","auto");
    var anchorString = "";
    for (var i=0;i<this.items.length;i++) {
      var cite = new andre.Citation(this.store,this.items[i]);
      if (i == 0) {
        anchorString += cite.shortString();
      } else if (i == this.items.length - 1) {
        anchorString += " + " + i + " more...";
      }
      // add the citation to the content element
      var c = content.appendChild(dojo.doc.createElement("div"));
      dojo.addClass(c,"citation-block");
      if (i == this.items.length - 1) { dojo.addClass(c,"citation-block-last"); }
      c.innerHTML = cite.fullString();
    }
    //console.debug(anchorString);
    // and make the anchored data display
    var expItem =  andre.utils.createAnchoredExpandingItem(id,anchorString,content);
    element.appendChild(expItem);
    return element;
  },
  /* returns a string containing the short display of this citation data */
  toStringShort: function() {
    // make sure our items are still in the store ???
    dojo.forEach(this.items,function(item,index,items) {
      if (!this.store.isItem(item)) {
        console.debug("Citation item no longer in store?");
        return "";
      }
    });
    // sort items 
    this.sortItems();
    // create the main element for this data
    var anchorString = "";
    for (var i=0;i<this.items.length;i++) {
      var cite = new andre.Citation(this.store,this.items[i]);
      if (i == 0) {
        anchorString += cite.shortString();
      } else if (i == this.items.length - 1) {
        anchorString += " + " + i + " more...";
      }
    }
    //console.debug(anchorString);
    return anchorString;
  },
  /* returns a single DOM node containing the short display of this citation data */
  toNodeShort: function() {
    // create the main element for this data
    var element = dojo.doc.createElement("span");
    dojo.addClass(element,"short-citation-container");
    element.innerHTML = this.toStringShort();
    return element;
  },
  /* returns a single DOM node containing the full description of this citation data */
  toNode: function() {
    // make sure our items are still in the store ???
    dojo.forEach(this.items,function(item,index,items) {
      if (!this.store.isItem(item)) {
        console.debug("Citation item no longer in store?");
        return null;
      }
    });
    // sort items 
    this.sortItems();
    // create the main element for this data
    var element = dojo.doc.createElement("div");
    dojo.addClass(element,"citation-container");
    for (var i=0;i<this.items.length;i++) {
      var cite = new andre.Citation(this.store,this.items[i]);
      // add the citation to the element
      var c = element.appendChild(dojo.doc.createElement("div"));
      dojo.addClass(c,"citation-block");
      if (i == this.items.length - 1) { dojo.addClass(c,"citation-block-last"); }
      c.innerHTML = cite.fullString();
    }
    return element;
  },
  sortItems: function() {
    // sort items in the list so they're always the same
    // FIXME: doesn't really matter what the order is as long as its always the same? for now, sort newest -> oldest
    this.items.sort(function(a,b) {
      var aN = this.store.getValue(a,"year");
      var bN = this.store.getValue(b,"year");
      if ((bN - aN) != 0) {
        return (bN-aN);
      } else {
        aN = 0;
        bN = 0;
        if (this.store.hasAttribute(a,"month")) { 
          aN = this.store.getValue(a,"month");
        }
        if (this.store.hasAttribute(b,"month")) { 
          bN = this.store.getValue(a,"month");
        }
        if ((bN - aN) != 0) {
          return (bN-aN);
        } else {
          aN = 0;
          bN = 0;
          if (this.store.hasAttribute(a,"day")) { 
            aN = this.store.getValue(a,"day");
          }
          if (this.store.hasAttribute(b,"day")) { 
            bN = this.store.getValue(a,"day");
          }
          return (bN - aN);
        }
      }
    });
  }
});

/* to handle a single citation */
dojo.declare("andre.Citation", null, {
  authors: [],
  year: -1,
  month: -1,
  day: -1,
  title: "",
  doi: "",
  journal: "",
  /* pages (and volumes?) are not always numerical */
  startPage: "",
  endPage: "",
  volume: "",
  number: "",
  bibliographicCitation: "",
  constructor: function(store,item) {
    //console.debug("Making a new citation object");
    if (store.isItem(item)) {
      //console.debug("Item is in the store (" + store.getValue(item,"uri") + ")");
      if (store.hasAttribute(item,"authors")) {
        //console.debug("authors present");
        this.authors = store.getValues(item,"authors");
        //console.debug("found " + this.authors.length + " authors");
      } else {
        console.debug("ERROR: no authors found?");
      }
      this.year = store.getValue(item,"year");
      this.journal = store.getValue(item,"journal");
      this.title = store.getValue(item,"title");
      if (store.hasAttribute(item,"month")) {
        this.month= store.getValue(item,"month");
      }
      if (store.hasAttribute(item,"day")) {
        this.day = store.getValue(item,"day");
      }
      if (store.hasAttribute(item,"doi")) {
        this.doi = store.getValue(item,"doi");
      }
      if (store.hasAttribute(item,"startPage")) {
        this.startPage = store.getValue(item,"startPage");
      }
      if (store.hasAttribute(item,"endPage")) {
        this.endPage = store.getValue(item,"endPage");
      }
      if (store.hasAttribute(item,"volume")) {
        this.volume = store.getValue(item,"volume");
      }
      if (store.hasAttribute(item,"number")) {
        this.number = store.getValue(item,"number");
        //console.debug("number found: " + this.number);
      }
      if (store.hasAttribute(item,"bibliographicCitation")) {
        this.bibliographicCitation = store.getValue(item,"bibliographicCitation");
      }
    }
  },
  shortString: function() {
    var str = this.authors[0];
    if (this.authors.length > 2) {
      str += " <i>et al</i>";
    } else if (this.authors.length == 2) {
      str += " &amp; " + this.authors[1];
    }
    str += " (" + this.year + ")";
    return str;
  },
  fullString: function() {
    var str = "";
    for (var i=0; i < this.authors.length; i++) {
      if (i > 0 && i != (this.authors.length - 1)) {
        str += ", ";
      } else if (i == this.authors.length - 1) {
        str += " &amp; ";
      }
      str += this.authors[i];
    }
    str += ". &apos;";
    if (this.doi != "") {
      str += "<a href=\"http://dx.doi.org/" + this.doi + "\">";
    }
    str += this.title;
    if (this.doi != "") {
      str += "</a>";
    }
    str += "&apos;. ";
    if (this.bibliographicCitation != "") {
      // FIXME: hack for csim:citations
      str += "<em>" + this.bibliographicCitation + "</em>";
    } else {
      str += "<em>" + this.journal + "</em>, ";
      str += "<b>" + this.volume + "</b>";
      if (this.number != "") {
        str += "(" + this.number + ")";
      }
      str += ":&nbsp;" + this.startPage + "&mdash;" + this.endPage + ", " + this.year + ".";
    }
    return str;
  }
});
