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
  Define a class to handle reference descriptions - a wrapper for all the other modules.
*/
dojo.provide("andre.ReferenceDescription");
dojo.require("dijit.Tree");
dojo.require("dojox.fx.easing");
dojo.require("dojox.fx.scroll");
dojo.require("andre.utils");
dojo.require("andre.Date");
dojo.require("andre.ContentItemDisplay");
dojo.declare("andre.ReferenceDescription", null, {
  store: null,
  root: null,
  headerNode: null,
  taskNode: null,
  contentNode: null,
  footerNode: null,
  /* the base URL of the source data for this reference description */
  srcBaseURL: null,
  /* constructor simply saves the items and its store so that data can be fetched out as required */
  constructor: function(store, item, headerNode, taskNode, contentNode, footerNode, srcBaseURL) {
    this.store = store;
    this.root = item;
    this.headerNode = headerNode;
    this.taskNode = taskNode;
    this.contentNode = contentNode;
    this.footerNode = footerNode;
    this.srcBaseURL = srcBaseURL;
  },
  /* initialise the given document nodes for this reference description */
  initialiseDocument: function() {
    // clear the content of the document nodes FIXME: how should this be done?
    this.headerNode.innerHTML = "";
    this.taskNode.innerHTML = "";
    this.contentNode.innerHTML = "";
    this.footerNode.innerHTML = "";
    // set the document header
    this._setDocumentHeader(this.headerNode);
    console.log("header initialised");
    // set the document footer
    this._setDocumentFooter(this.footerNode);
    console.log("footer initialised");
    // create the task/graph tree in the task pane
    this._createTaskListing(this.taskNode);
    console.log("task list initialised");
    // and add the root item to the content pane display
    var id = this.store.getIdentity(this.root);
    this.displayContentItem(id);
    console.log("root item displayed");
  },
  /* display a content item in the content pane:
      - if its already displayed, shift focus to it;
      - if its not displayed but exists (display: none) place it and display it as below FIXME: will never occur now?
      - if display doesn't exist, create the display and add it to the content pane
        - if 'context' is not null, insert below the context
        - otherwise insert at the top of the content pane
  */
  displayContentItem: function(/*String*/id,/*String*/parentId) {
    console.debug("Displaying content: " + id + " using " + parentId + " as context");
    var context = parentId ? dijit.byId(parentId) : null;
    // FIXME: the scope of this changes to the window (?) inside here...
    var myself = this;
    this.store.fetchItemByIdentity({
      identity: id,
      onItem: function(item,request) {
        // if we have a variable, we want to ensure we only ever display source variables
        if (myself.store.getValue(item,"type") == "variable") {
          if (myself.store.hasAttribute(item,"sourceVariable")) {
            console.log("Displaying a non-source variable, swapping to source variable");
            var sourceVariable = myself.store.getValue(item,"sourceVariable");
            item = sourceVariable;
          }
        }
        var id = myself.store.getIdentity(item);
        var currentDijit = dijit.byId(id);
        if (currentDijit) {
          console.debug("Found content item, switching focus");
          //currentDijit.focus();
        } else {
          console.debug("Content item doesn't exist, so creating");
          currentDijit = new andre.ContentItemDisplay({store: myself.store, item: item, srcBaseURL: myself.srcBaseURL});
          if (context) {
            currentDijit.addToDocument(context.domNode,"after");
          } else {
            currentDijit.addToDocument(myself.contentNode,"first");
          }
          //currentDijit.focus();
        }
        dijit.scrollIntoView(currentDijit.domNode);
        andre.utils.highlightNode(currentDijit.domNode);
        /*dojox.fx.smoothScroll({
          node: currentDijit.domNode,
          win: myself.contentNode,
          duration: 300
        }).play();*/
      },
      onError: function(error,request) {
        var msg = "ERROR: problem getting the content item: " + id + " to display";
        var e = dojo.doc.createElement("div");
        dojo.addClass(e,"error-message");
        e.appendChild(dojo.doc.createTextNode(msg));;
        if (context) {
          dojo.place(e,context.domNode,"after");
        } else {
          dojo.place(e,this.contentNode,"first");
        }
        console.log(msg);
      }
    });
  },
  /* creates the reference description page header as a child of the given node. Also sets the window title */
  _setDocumentHeader: function(node) {
    var title = "Untitled";
    if (this.store.hasAttribute(this.root,"title")) title = this.store.getValue(this.root,"title");
    dojo.doc.title = title;
    // add a link to the help dialog, if one is defined?
    var helpDialog = dijit.byId("help-dialog");
    if (helpDialog) {
      var link = node.appendChild(dojo.doc.createElement("a"));
      dojo.addClass(link,"help-link");
      dojo.addClass(link,"helpIcon");
      link.setAttribute("href","javascript:;");
      link.setAttribute("onclick","dijit.byId('help-dialog').show()");
      link.innerHTML = "Help";
    }
    // create a container for the header
    var element = node.appendChild(dojo.doc.createElement("div"));
    var id = this.store.getIdentity(this.root);
    var uri = this.store.getValue(this.root,"uri");
    element.setAttribute("id",id + "-page-header");
    dojo.addClass(element,"page-header");
    element.setAttribute("onclick","displayContentItem('"+id+"')");
    var e = element.appendChild(dojo.doc.createElement("h1"));
    dojo.addClass(e,"document-title");
    e.appendChild(dojo.doc.createTextNode(title));
    /* add in the brief version of the creation data */
    if (this.store.hasAttribute(this.root,"created")) {
      e = new andre.CreationData(this.store,this.store.getValue(this.root, "created"));
      if (e) {
        element.appendChild(e.toDOMNodeBrief());
      } else {
        console.debug("ERROR: problem with creation data?");
      }
    }
  },
  /* set the page footer */
  _setDocumentFooter: function(node) {
    var element = node.appendChild(dojo.doc.createElement("span"));
    var id = this.store.getIdentity(this.root);
    element.setAttribute("id",id + "-page-footer");
    dojo.addClass(element,"page-footer");
    if (this.store.hasAttribute(this.root,"generated")) {
      var generated = this.store.getValue(this.root,"generated");
      if (this.store.hasAttribute(generated,"tool")) {
        var tool = this.store.getValue(generated,"tool");
        var uri = "";
        if (this.store.hasAttribute(generated,"uri")) uri = this.store.getValue(generated,"uri");
        var e = element.appendChild(dojo.doc.createElement("span"));
        e.appendChild(dojo.doc.createTextNode("Generated by: "));
        var a = e;
        if (uri != "") {
          a = e.appendChild(dojo.doc.createElement("a"));
          a.setAttribute("href",uri);
          a.setAttribute("target","_blank");
        }
        a.appendChild(dojo.doc.createTextNode(tool));
      }
      if (this.store.hasAttribute(generated,"version")) {
        var version = this.store.getValue(generated,"version");
        var e = element.appendChild(dojo.doc.createElement("span"));
        e.appendChild(dojo.doc.createTextNode(" (version: " + version + ")"));
      }
      if (this.store.hasAttribute(generated,"date")) {
        var str = this.store.getValue(generated,"date");
        var d = new andre.Date(str);
        var generatedAt = d.fullString();
        var e = element.appendChild(dojo.doc.createElement("span"));
        e.appendChild(dojo.doc.createTextNode(" at " + generatedAt));
      }
    }
  },
  
  _createTaskListing: function(node) {
    // summary: within the given node, create a listing of all the tasks and graphs of the reference description
    var model = new dijit.tree.TreeStoreModel({
      store: this.store,
      /* can fake a root node if required, need to remove the showRoot below as well */
      //rootId: "http://cellml.sourceforge.net/#FakeRootNode",
      //rootLabel: "Root Item",
      query: {type: "root"},
      childrenAttrs: ["tasks","graphs"]
    });
    var id = "reference-description-task-listing-tree";
    var tree = new dijit.Tree({
      id: id,
      showRoot: true,
      model: model,
      /* onClick doesn't seem to keep with 'this' scope?
      onClick: this._taskListItemSelected*/
      getIconClass: this._getIconClass,
    });
    node.appendChild(tree.domNode);
    tree.startup();
    // subscribe to the onClick event - will never unsubscribe?
    dojo.subscribe(id,this,"_taskListItemSelected");
  },
  /* callback for clicking on an item in the task listing */
  _taskListItemSelected: function(message) {
    /* get the message contents */
    var tree = message.tree;
    var event = message.event;
    var item = message.item;
    var node = message.node;
    var id = this.store.getIdentity(item);
    console.debug("Task list item '" + event + "': " + id);
    this.displayContentItem(id);
  },
  /* callback to override the default icons used in the tree, again, 'this' is now the dijit.Tree */
  _getIconClass: function(item,opened) {
    var store = this.model.store;
    if (item && store.hasAttribute(item,"type")) {
      var type = store.getValue(item,"type");
      if (type == "root") {
        if (this.model.mayHaveChildren(item)) {
          return (opened ? "treeRootExpanded" : "treeRootCollapsed");
        } else {
          return "taskIcon";
        }
      } else if (type == "task") {
        if (this.model.mayHaveChildren(item)) {
          return (opened ? "treeBranchExpanded" : "treeBranchCollapsed");
        } else {
          return "taskIcon";
        }
      } else if (type == "graph") {
        // FIXME: a graph will never have children?
        return "graphIcon";
      }
    }
    // default
    return (!item || this.model.mayHaveChildren(item)) ? (opened ? "dijitFolderOpened" : "dijitFolderClosed") : "dijitLeaf"
  },
});
