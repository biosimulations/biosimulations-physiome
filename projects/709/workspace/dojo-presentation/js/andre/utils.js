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
  Various utilities until I work out a better module structure
 */
dojo.provide("andre.utils");

/* required includes */
dojo.require("andre.InlineTitlePane");
dojo.require("andre.CitationData");
dojo.require("andre.CreationData");
dojo.require("andre.ModificationData");
dojo.require("andre.DataStore");

dojo.require("dojox.fx");
//dojo.require("dojo.fx.easing");
//dojo.require("dojox.fx.scroll");

/* a function to create a text anchor which when clicked expands to the provided full content defined in the provided dom node.
FIXME: for now simply use a title pane dijit but could "easily" replace with a custom version of the title pane which has:
  - custom CSS
  - the title is as long as the text and expands sideways as the pane toggles
*/
andre.utils.createAnchoredExpandingItem = function(id,anchorString,/*dom node*/content) {
  console.debug("expanding anchor text: " + anchorString);
  var container = dojo.doc.createElement("div");
  dojo.addClass(container,"anchoredExpandingItemContainer");
  container.setAttribute("id",id + "--anchoredExpandingItemContainer");
  container.appendChild(content);
  var tp = new andre.InlineTitlePane({title: anchorString,open: false},container)
  return tp.domNode;
}

andre.utils.highlightNode = function(id) {
  // summary: a function which will focus on the given node and highlight it for a brief period
  console.log("Highlight node: " + id);
  var node = dojo.byId(id);
  dijit.scrollIntoView(node);
  /* FIXME: this isn't working very well... */
  /* looks like this scrolls to the middle of the element by default? */
  //var targetCoords = dojo.coords(node,true);
  //targetCoords.y -= targetCoords.h / 2;
  /*dojox.fx.smoothScroll({
    node: node,
    //target: targetCoords,
    win: dojo.byId('content-pane'),
    duration: 300,
    easing: dojo.fx.easing.easeOut
  }).play();*/
  dojox.fx.highlight({
    node: id,
    /*color: '#ffff99',*/ /* default = #ffff99 (light yellow) */
    duration: 500, /* default = 400 */
  }).play();
}

andre.utils.getContentItemLinkText = function(/*String*/id, /*String*/ctxId, /*String*/text) {
  // summary: common method for defining the link string for connecting to a different content item
  // id: the ID of the content item to link to
  // ctxId: the id of the context node for adding the content item to the display
  // text: the displayed body of the link
  var str = "<a href='javascript:;' onclick='displayContentItem(\"" + id + "\",\"" + ctxId + "\");'>" + text + "</a>";
  return str;
}

andre.utils.makeContentItemLink = function(/*String*/id, /*String*/ctxId, /*String*/text, /*Sting*/type) {
  // summary: common method for creating a link to a specific content item. Returns the created element.
  // id: the ID of the content item to link to
  // ctxId: the id of the context node for adding the content item to the display
  // text: the displayed body of the link
  // type: the type of the destination content item
  var link = dojo.doc.createElement("a");
  dojo.addClass(link,"andreContentItemLink");
  link.setAttribute("href","javascript:;");
  // the type specific icon
  dojo.addClass(link,andre.utils.getIconClass(type));
  link.setAttribute("onclick","displayContentItem(\"" + id + "\",\"" + ctxId + "\");");
  link.innerHTML = text;
  return link;
}

andre.utils.makeContentItemLinkFromItem = function(/*DataStore*/store, /*DataItem*/item, /*String*/ctxId) {
  // summary: create a content item link from the given data item
  var title = "Unknown";
  if (store.hasAttribute(item,"title")) title = store.getValue(item,"title");
  var type = "unknown";
  if (store.hasAttribute(item,"type")) type = store.getValue(item,"type");
  var id = store.getIdentity(item);
  if (type == "component") {
    // need to get the root import component
    var imports = andre.utils.getComponentImportList(store,item);
    var c = imports.pop();
    if (store.hasAttribute(c,"title")) title = store.getValue(c,"title");
  }
  return andre.utils.makeContentItemLink(id, ctxId, title, type);
}

andre.utils.makeContentItemLinkFromURI = function(/*DataStore*/store, /*String*/uri, /*String*/ctxId) {
  // summary: a method create the content item link from a content item found in the data store with a matching URI value
  console.log("Making content item link from the URI: " + uri);
  var link = null;
  store.fetch({
    query: {uri: uri},
    onComplete: function(items,request) {
      // we only want the first one?
      var item = items[0];
      if (store.isItem(item)) {
        var title = "unknown";
        if (store.hasAttribute(item,"title")) title = store.getValue(item,"title");
        var type = "unknown";
        if (store.hasAttribute(item,"type")) type = store.getValue(item,"type");
        link = andre.utils.makeContentItemLink(store.getIdentity(item), ctxId, title, type);
      } else {
        console.log("Invalid item for this store?");
      }
    },
    onError: function(error,request) {
      console.debug("(makeContentItemLinkFromURI): The request failed: " + error);
    }
  });
  if (link == null) {
    link  = dojo.doc.createElement("span");
    dojo.addClass(link,"error-message");
    link.innerHTML = "There was a problem";
  }
  return link;
}

andre.utils.getIconClass = function(/*String*/type) {
  if ((type == "root") || (type == "task")) {
    return "taskIcon";
  } else if (type == "graph") {
    return "graphIcon";
  } else if (type == "simulation") {
    return "simulationIcon";
  } else if (type == "model") {
    return "modelIcon";
  } else if (type == "component") {
    return "componentIcon";
  } else if (type == "variable") {
    return "variableIcon";
  } else {
    return "unknownIcon";
  }
}

andre.utils.getComponentImportList = function(/*DataStore*/store, /*DataItem*/component) {
  // summary: for the given component object, trace back through imports and return the list of component objects
  //console.debug("andre.utils.getComponentImportList called");
  var components = new Array(component);
  if (store.hasAttribute(component,"importedAs"))
  {
    var importComponent = store.getValue(component,"importedAs");
    var imports = andre.utils.getComponentImportList(store,importComponent);
    dojo.forEach(imports, function(i) {
      components.push(i);
    });
  }
  return components;
}
