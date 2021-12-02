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
/* a widget used to contain a content item */
dojo.provide("andre.ContentItemDisplay");
dojo.require("dojo.fx");
dojo.require("dojox.layout.ContentPane");
dojo.require("andre.CitationData");
dojo.require("andre.CreationData");
dojo.require("andre.ModificationData");
dojo.require("andre.InlineTitlePane");
dojo.require("andre.ClosablePane");
dojo.require("andre.Chart");
dojo.declare("andre.ContentItemDisplay", andre.ClosablePane, {
  store: null,
  item: null,
  srcBaseURL: null,
  
  // chart: andre.Chart
  //  Will be the chart object if this is a graph content item.
  chart: null,
  
  // chartContainer: DomNode
  //  Inserted into the page to hold the chart, if any, as a place holder for when we are ready to position the chart to the correct location within the page flow.
  chartContainer: null,
  
  postMixInProperties: function () {
    // make sure the id is set correctly, we want the ensure that we can always refer to this dijit via it's data store identity.
    this.id = this.store.getIdentity(this.item);
    // and set the (initial?) title
    if (this.store.hasAttribute(this.item,"title")) {
      this.heading = this.store.getValue(this.item,"title");
    } else {
      this.showHeading = false;
      if (this.heading == "") this.heading = "Untitled content item";
    }
    // and set up the type
    if (this.store.hasAttribute(this.item,"type")) this.type = this.store.getValue(this.item,"type");
    else {
      console.debug("ERROR: missing type on content item");
      this.type = "unknown";
    }
    // and the type specific icon
    this.iconClass = andre.utils.getIconClass(this.type);
    this.iconClass += " contentItemIcon";
  },
  
  postCreate: function() {
    // Populate the containerNode of the closable pane
    console.log("andre.ContentItemDisplay.postCreate() called for: " + this.id);
    this.inherited(arguments);
    // First add the standard annotations
    if (this.type != "component") {
      this._appendCommonAnnotations(this.item,this.containerNode,true);
    } else {
      // for components we want to use the ultimate import parent component
      var imports = andre.utils.getComponentImportList(this.store,this.item);
      var c = imports.pop();
      this._appendCommonAnnotations(c,this.containerNode,true);
    }
    // and now type specific
    if ((this.type == "root") || (this.type == "task")) {
      this._appendTaskContent();
    } else if (this.type == "graph") {
      this._appendGraphContent();
    } else if (this.type == "simulation") {
      this._appendSimulationContent();
    } else if (this.type == "model") {
      this._appendModelContent();
    } else if (this.type == "component") {
      this._appendComponentContent();
    } else if (this.type == "variable") {
      this._appendVariableContent();
    }
  },
  
  /* we need this as the tabContainer.startup() method must be called after the tab container has been inserted into the page body. */
  addToDocument: function(refNode,position) {
    console.debug("adding to document in position: " + position);
    dojo.style(this.domNode,"opacity","0");
    dojo.place(this.domNode,refNode,position);
    // move the chart, if any, to the correct location
    if (this.chart) {
      this.chart.place(this.chartContainer,"first");
    }
    dojo.fadeIn({node: this.domNode, duration: 500}).play();
  },
  _appendCommonAnnotations: function(/*StoreItem*/item, /*DomNode*/parent, /*Bool*/updateHeader) {
    // summary: append the common annotations to the current content item
    // item: the data store item to use to look for commom annotations; we provide this here as we may not always want to use the content item's 'item' attribute (i.e., in the case of components).
    // the base ID to use on all items
    var baseID = this.store.getIdentity(item);
    if (updateHeader) {
      // update the title (in case item is different to this.item)
      if (this.store.hasAttribute(item,"title")) {
        this.setHeading(this.store.getValue(item,"title"));
      }
    }
    // put the common annotations into their own container
    var annotation = parent.appendChild(dojo.doc.createElement("div"));
    dojo.addClass(annotation,"content-item-common-annotation");
    // then the citation inline title pane
    if (this.store.hasAttribute(item,"citations")) {
      e = new andre.CitationData(this.store, this.store.getValues(item,"citations"));
      if (e) {
        var references = annotation.appendChild(dojo.doc.createElement("div"));
        references.appendChild(e.toNode());
        // and create the dijit
        var itp = new andre.InlineTitlePane({title: e.toStringShort(), open: false, id: baseID + "-references-dijit"},references);
      } else {
        console.debug("Error getting the citations data in a DOM node");
      }
    }
    // followed by the history title pane
    var historyTitle = "";
    var history = null;
    if (this.store.hasAttribute(item,"created")) {
      e = new andre.CreationData(this.store, this.store.getValue(item,"created"));
      if (e) {
        history = annotation.appendChild(dojo.doc.createElement("div"));
        history.appendChild(e.toNode());
        historyTitle = e.toStringShort();
      } else {
        console.debug("Error getting the created data in a DOM node");
      }
    }
    if (this.store.hasAttribute(item,"modifications")) {
      e = new andre.ModificationData(this.store, this.store.getValues(item,"modifications"));
      if (e) {
        if (!history) history = annotation.appendChild(dojo.doc.createElement("div"));
        history.appendChild(e.toNode());
        historyTitle = e.toStringShort() + " (" + historyTitle + ")";
      } else {
        console.debug("Error getting the modifications data in a DOM node");
      }
    }
    if (history) {
      var itp = new andre.InlineTitlePane({title: historyTitle, open: false, id: baseID + "-history-dijit"}, history);
    }
    // other relevant data?
    if (this.store.hasAttribute(item,"species")) {
      e = parent.appendChild(dojo.doc.createElement("div"));
      dojo.addClass(e,"content-item-species-annotation");
      e.appendChild(dojo.doc.createElement("span")).innerHTML = "Species: ";
      e.appendChild(dojo.doc.createElement("i")).innerHTML = this.store.getValue(item,"species");
    }
    if (this.store.hasAttribute(item,"bio_entity")) {
      e = parent.appendChild(dojo.doc.createElement("div"));
      dojo.addClass(e,"content-item-bioe_entity-annotation");
      e.appendChild(dojo.doc.createElement("span")).innerHTML = "Biological Entity: ";
      e.appendChild(dojo.doc.createElement("span")).innerHTML = this.store.getValue(item,"bio_entity");
    }
    // an abstract?
    if (this.store.hasAttribute(item,"abstract")) {
      e = parent.appendChild(dojo.doc.createElement("div"));
      dojo.addClass(e,"content-item-abstract");
      e.innerHTML = this.store.getValue(item,"abstract");
    }
    // any description?
    if (this.store.hasAttribute(item,"description")) {
      e = parent.appendChild(dojo.doc.createElement("div"));
      dojo.addClass(e,"content-item-description");
      e.innerHTML = this.store.getValue(item,"description");
    }
  },
  _appendTaskContent: function() {
    // summary: add task specific content to the content item display
    console.debug("_appendTaskContent called");
    var childrenTypes = ["tasks","graphs"];
    var childrenHeadings = ["Tasks:","Defined Graphs:"];
    for (var t = 0;t<childrenTypes.length;t++) {
      if (this.store.hasAttribute(this.item,childrenTypes[t])) {
        var tasks = this.store.getValues(this.item,childrenTypes[t]);
        if (tasks.length > 0) {
          var element = this.containerNode.appendChild(dojo.doc.createElement("div"));
          dojo.addClass(element,"content-item-sub-content-container");
          var e = element.appendChild(dojo.doc.createElement("h3"));
          dojo.addClass(e,"content-item-sub-header");
          e.innerHTML = childrenHeadings[t];
          var ul = element.appendChild(dojo.doc.createElement("ul"));
          for (var i=0;i<tasks.length;i++) {
            e = ul.appendChild(dojo.doc.createElement("li"));
            var text = "Anonymous";
            if (this.store.hasAttribute(tasks[i],"title")) {
              text = this.store.getValue(tasks[i],"title");
            }
            e.appendChild(andre.utils.makeContentItemLink( this.store.getIdentity(tasks[i]), this.id, text, childrenTypes[t] == "tasks" ? "task" : "graph"));
          }
        }
      }
    }
  },
  _appendGraphContent: function() {
    // summary: add graph specific content to the content item display
    console.debug("_appendGraphContent called with srcBaseURL set to: " + this.srcBaseURL);
    // create a container to hold the graph information
    this.chartContainer = this.containerNode.appendChild(dojo.doc.createElement("div"));
    dojo.addClass(this.chartContainer,"graph-container");
    // assemble the style object for the graph
    var style = {};
    style.width = "400px";
    style.height = "400px";
    if (this.store.hasAttribute(this.item,"background")) {
      style.backgroundColor = this.store.getValue(this.item,"background");
    }
    if (this.store.hasAttribute(this.item,"colour")) {
      style.color = this.store.getValue(this.item,"colour");
    }
    if (this.store.hasAttribute(this.item,"csvSource")) {
      var titles = {};
      if (this.store.hasAttribute(this.item,"title")) titles.title = this.store.getValue(this.item,"title");
      if (this.store.hasAttribute(this.item,"xLabel")) titles.x = this.store.getValue(this.item,"xLabel");
      if (this.store.hasAttribute(this.item,"yLabel")) titles.y = this.store.getValue(this.item,"yLabel");
      /* FIXME: should encode the generated CSV file URL into the JSON source for the reference description */
      var csvURL = this.srcBaseURL + this.store.getValue(this.item,"csvSource");
      this.chart = new andre.Chart(this.id, csvURL, style, titles);
      if (this.store.hasAttribute(this.item,"traces")) {
        var traces = this.store.getValues(this.item,"traces");
        dojo.forEach(traces, function(trace,i) {
          var style = {};
          if (this.store.hasAttribute(trace,"colour")) {
            style.stroke = this.store.getValue(trace,"colour");
          }
          if (this.store.hasAttribute(trace,"label")) {
            this.chart.addSeriesByLabel(this.store,trace,style);
          } else {
            this.chart.addSeriesByPosition((i+1).toString(),style);
          }
        }, this);
      } else {
        console.log("ERROR: No traces in graph?");
      }
    } else {
      console.log("ERROR: No data for graph?");
    }
  },
  
  _appendSimulationContent: function() {
    // summary: add simulation specific content to the content item display
    console.debug("_appendSimulationContent called");
    // create a container to hold the simulation information
    var container = this.containerNode.appendChild(dojo.doc.createElement("div"));
    dojo.addClass(container,"simulation-container");
    // a simple header?
    container.appendChild(dojo.doc.createElement("h3")).appendChild(dojo.doc.createTextNode("Simulation definition"));
    // put the definition in a definition list
    var dl = container.appendChild(dojo.doc.createElement("dl"));
    dojo.addClass(dl,"simulation-definition");
    // must have a model reference
    dl.appendChild(dojo.doc.createElement("dt")).appendChild(dojo.doc.createTextNode("Model"));
    var model = this.store.getValue(this.item,"model");
    // and the model should have a title?
    var title = "Untitled";
    if (this.store.hasAttribute(model,"title")) title = this.store.getValue(model,"title");
    var id = this.store.getIdentity(model);
    dl.appendChild(andre.utils.makeContentItemLink(id, this.id, title, "model"));
    // and a bound interval
    dl.appendChild(dojo.doc.createElement("dt")).appendChild( dojo.doc.createTextNode("Bound Interval"));
    var interval = this.store.getValue(this.item,"boundInterval");
    // which will have a variable reference
    var variable = this.store.getValue(interval,"variable");
    dl.appendChild(dojo.doc.createElement("dd")).appendChild( andre.utils.makeContentItemLinkFromURI(this.store, variable, this.id));
    // the integration parameters
    dl.appendChild(dojo.doc.createElement("dd")).innerHTML = "Starting value: " + this.store.getValue(interval,"start");
    dl.appendChild(dojo.doc.createElement("dd")).innerHTML = "Ending value: " + this.store.getValue(interval,"end");
    dl.appendChild(dojo.doc.createElement("dd")).innerHTML = "Maximum step size: " + this.store.getValue(interval,"maximumStepSize");
    dl.appendChild(dojo.doc.createElement("dd")).innerHTML = "Tabulation step size: " + this.store.getValue(interval,"tabulationStepSize");
    // and finally the numerical methods
    dl.appendChild(dojo.doc.createElement("dt")).appendChild( dojo.doc.createTextNode("Numerical Methods"));
    var numericalMethods = this.store.getValue(this.item,"numericalMethods");
    dl.appendChild(dojo.doc.createElement("dd")).innerHTML = "Multistep method: " + this.store.getValue(numericalMethods,"multistepMethod");
    dl.appendChild(dojo.doc.createElement("dd")).innerHTML = "Iteration method: " + this.store.getValue(numericalMethods,"iterationMethod");
    dl.appendChild(dojo.doc.createElement("dd")).innerHTML = "Linear solver: " + this.store.getValue(numericalMethods,"linearSolver");
  },
  
  _appendModelContent: function() {
    // summary: add model specific content to the content item display
    console.debug("_appendModelContent called");
    // create a container to hold the model information
    var container = this.containerNode.appendChild(dojo.doc.createElement("div"));
    dojo.addClass(container,"model-container");
    // the only model content is a list of components?
    if (this.store.hasAttribute(this.item,"components")) {
      var components = this.store.getValues(this.item,"components");
      if (components.length > 0) {
        var e = container.appendChild(dojo.doc.createElement("h3"));
        dojo.addClass(e,"content-item-sub-header");
        e.innerHTML = "Math Containers";
        var ul = container.appendChild(dojo.doc.createElement("ul"));
        dojo.forEach(components, function(component,i) {
          e = ul.appendChild(dojo.doc.createElement("li"));
          // component is the actual unique component we want to link to, but we want to display the title of the ultimate import parent as a more meaningful link text to display to the user
          var imports = andre.utils.getComponentImportList(this.store,component);
          var c = imports.pop();
          var title = "Anonymous";
          if (this.store.hasAttribute(c,"title")) title = this.store.getValue(c,"title");
          e.appendChild(andre.utils.makeContentItemLink(this.store.getIdentity(component), this.id, title, "component"));
        }, this);
      }
    }
  },
  
  _appendComponentContent: function() {
    // summary: append component specific content
    // if this is a component that has been imported we want to provide access to any data associated with any of the imported instances
    if (this.store.hasAttribute(this.item,"importedAs")) {
      var container = this.containerNode.appendChild(dojo.doc.createElement("div"));
      dojo.addClass(container,"imported-as-container");
      var imports = andre.utils.getComponentImportList(this.store,this.item);
      // we already have the annotations from the ultimate parent component so we can disregard that one
      imports.pop();
      // now we walk our way back to this component
      this._appendComponentImportedAsContent(imports,container);
    }
    // and output the math from this component
    if (this.store.hasAttribute(this.item,"math")) {
      var math = dojo.doc.createElement("object");
      dojo.addClass(math,"math-container");
      var mathURL = this.srcBaseURL + this.store.getValue(this.item,"math");
      math.setAttribute("data",mathURL);
      math.setAttribute("type","application/xhtml+xml");
      this.containerNode.appendChild(math);
    }
  },
  _appendComponentImportedAsContent: function(/*Array*/imports, /*DomNode*/node) {
    // summary: walk back through the imported-as components adding the annotations as children of the given 
    while (imports.length > 0) {
      var c = imports.pop();
      var container = node.appendChild(dojo.doc.createElement("div"));
      dojo.addClass(container,"imported-as-component");
      //var e = container.appendChild(dojo.doc.createElement("div"));
      //dojo.addClass(e,"imported-as-component-header");
      var title = "Untitled";
      if (this.store.hasAttribute(c,"title")) title = this.store.getValue(c,"title");
      //e.innerHTML = "Imported from: " + title;
      this._appendCommonAnnotations(c,container,false);
      var itp = new andre.InlineTitlePane({title: "Imported from: " + title, open: false},container);
    }
  },
  
  _appendVariableContent: function() {
    // summary: append variable specific data to the content item display
    console.log("appending variable content");
    var div = this.containerNode.appendChild(dojo.doc.createElement("div"));
    if (this.store.hasAttribute(this.item,"initialValueVariable")) {
      div.appendChild(dojo.doc.createElement("b")).innerHTML = "Initial value: ";
      var ivV = this.store.getValue(this.item,"initialValueVariable");
      var title = "initial value variable";
      if (this.store.hasAttribute(ivV,"title")) title = this.store.getValue(ivV, "title");
      div.appendChild(andre.utils.makeContentItemLink(this.store.getIdentity(ivV), this.id, title, "variable"));
    } else if (this.store.hasAttribute(this.item,"initialValue")) {
      div.appendChild(dojo.doc.createElement("b")).innerHTML = "Initial value: ";
      div.appendChild(dojo.doc.createElement("span")).innerHTML = this.store.getValue(this.item,"initialValue");
    }
    div = this.containerNode.appendChild(dojo.doc.createElement("div"));
    div.appendChild(dojo.doc.createElement("b")).innerHTML = "Units: ";
    if (this.store.hasAttribute(this.item,"units")) {
      div.appendChild(dojo.doc.createElement("span")).innerHTML = this.store.getValue(this.item,"units");
    } else {
      div.appendChild(dojo.doc.createElement("span")).innerHTML = "unknown";
    }
    if (this.store.hasAttribute(this.item,"definedIn")) {
      var id = this.store.getValue(this.item,"definedIn");
      var div = this.containerNode.appendChild(dojo.doc.createElement("div"));
      var myself = this;
      this.store.fetchItemByIdentity({
        identity: id,
        onItem: function(item,request) {
          div.appendChild(dojo.doc.createElement("b")).innerHTML = "Defined in math container: ";
          div.appendChild(andre.utils.makeContentItemLinkFromItem(myself.store, item, myself.id));
        },
        onError: function(error,request) {
          var e = dojo.doc.createElement("div");
          dojo.addClass(e,"error-message");
          e.innerHTML = "Error getting math container link: " + error;
        }
      });
    }
    if (this.store.hasAttribute(this.item,"usedIn")) {
      console.log("Appending usedIn components");
      div = this.containerNode.appendChild(dojo.doc.createElement("div"));
      div.appendChild(dojo.doc.createElement("b")).innerHTML = "Used in math containers:";
      var ul = div.appendChild(dojo.doc.createElement("ul"));
      var usedInComponents = this.store.getValues(this.item,"usedIn");
      dojo.forEach(usedInComponents, function(usedIn,i) {
        var cID = usedIn[0];
        var vID = usedIn[1];
        var li = ul.appendChild(dojo.doc.createElement("li"));
        // the basic structure of the list element
        var componentSpan = li.appendChild(dojo.doc.createElement("span"));
        li.appendChild(dojo.doc.createTextNode(" as variable:"));
        var variableSpan = li.appendChild(dojo.doc.createElement("div"));
        var myself = this;
        // link to the math container where this variable is used
        this.store.fetchItemByIdentity({
          identity: cID,
          onItem: function(item,request) {
            componentSpan.appendChild(andre.utils.makeContentItemLinkFromItem(myself.store, item, myself.id));
          },
          onError: function(error,request) {
            var e = dojo.doc.createElement("div");
            dojo.addClass(e,"error-message");
            e.innerHTML = "Error getting math container link: " + error;
          }
        });
        // and the reference to the variable in that math container
        this.store.fetchItemByIdentity({
          identity: vID,
          onItem: function(item,request) {
            var title = "Unknown";
            if (myself.store.hasAttribute(item,"title")) title = myself.store.getValue(item,"title");
            myself._appendCommonAnnotations(item,variableSpan,false);
            var itp = new andre.InlineTitlePane({title: title, open: false}, variableSpan);
          },
          onError: function(error,request) {
            var e = dojo.doc.createElement("div");
            dojo.addClass(e,"error-message");
            e.innerHTML = "Error getting math container link: " + error;
          }
        });
        /*if (this.store.hasAttribute(this.item,"connectedVariables")) {
          var connectedVariables = this.store.getValues(this.item,"connectedVariables");
          var container = this.containerNode.appendChild(dojo.doc.createElement("div"));
          dojo.addClass(container,"variable-alias-container");
          container.appendChild(dojo.doc.createElement("h3")).innerHTML = "Also known as:";
          dojo.forEach(connectedVariables, function(variable) {
            var c = container.appendChild(dojo.doc.createElement("div"));
            dojo.addClass(c,"variable-alias");
            var title = "Unknown";
            if (this.store.hasAttribute(variable,"title")) title = this.store.getValue(variable,"title");
            this._appendCommonAnnotations(variable,c,false);
            var itp = new andre.InlineTitlePane({title: title, open: false}, c);
          }, this);
        }*/
      }, this);
    }
  },
  
  onClickCloseButton: function(event) {
    //console.dir(this);
    console.debug("onClickCloseButton: closing content item: " + this.id);
    // first fade out and set display to none - wipeOut will set display none
    var fadeTime = 500;
    var fade = dojo.fadeOut({node: this.domNode, duration: fadeTime});
    var wipe = dojo.fx.wipeOut({node: this.domNode, duration: fadeTime});
    dojo.fx.combine([fade, wipe]).play();
    // need to give the animation time to play out
    // FIXME: scope changes to window within here, so need to set what we need into local variables?
    var myself = this;
    setTimeout(function() {
      console.debug("onClickCloseButton: destroying content item: " + myself.id);
      // destroy the chart?
      if (this.chart) this.chart.destroy();
      // destroy all the dijit's first?
      myself.destroyRecursive();
      console.debug("onClickCloseButton: destroyed content item: " + myself.id);
    }, fadeTime);
  },
  
  onClickSourceButton: function(event) {
    console.debug("onClickSourceButton: view source of content item: " + this.id);
    if (this.store.hasAttribute(this.item,"uri")) {
      var uri = this.store.getValue(this.item,"uri");
      console.debug("view source at uri: " + uri);
      window.open(uri);
    } else {
      alert("Sorry, no source defined for this content item");
    }
  },
});
