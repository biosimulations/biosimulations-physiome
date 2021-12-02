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
dojo.provide("andre.ClosablePane");
dojo.require("dijit.form._FormWidget");
dojo.declare("andre.ClosablePane", dijit.form._FormWidget, {
  /*
  Summary:
          A closable content pane which may have a title. Also provides for animated insertion into a DOM document. Designed to be used as a wrapper around appended content???
          
          A _FormWidget has pretty much everything I need, so lets look at just using that?
  
  Start with a button and go from there...
  */
  
  // title: String
  //  text to display as the pane's title
  heading: "",

  // showTitle: Boolean
  //  whether or not to display the pane's title
  showHeading: true,

  // iconClass: String
  //  FIXME: maybe use this to put a icon next to the heading?
  iconClass: "",

  // FIXME: not sure what this will do?
  // FIXME: overridden by the content item display type attribute?
  type: "closable-pane",
  // the base CSS class for the dijit
  baseClass: "andreClosablePane",
  // and the template to use
  templatePath: dojo.moduleUrl("andre","templates/ClosablePane.html"),
  templateString: "",

  _onChangeMonitor: '',
  // TODO: set button's title to this.containerNode.innerText

  _onClick: function(/*Event*/ e){
    // summary: internal function to handle click actions
    if(this.disabled || this.readOnly){
      dojo.stopEvent(e); // needed for checkbox
      return false;
    }
    this._clicked(); // widget click actions
    return this.onClick(e); // user click actions
  },
  
  _onClickCloseButton: function (/*Event*/ e) {
    console.log("_Close button clicked for dijit: " + this.id);
    // summary: internal function to handle click actions
    if(this.disabled || this.readOnly) {
      console.log("dijit disabled, so do nothing");
      dojo.stopEvent(e);
      return false;
    }
    return this.onClickCloseButton(e); // user actions
  },
  
  _onClickSourceButton: function (/*Event*/ e) {
    console.log("_Source button clicked for dijit: " + this.id);
    // summary: internal function to handle click actions
    if(this.disabled || this.readOnly) {
      console.log("dijit disabled, so do nothing");
      dojo.stopEvent(e);
      return false;
    }
    return this.onClickSourceButton(e); // user actions
  },

  postCreate: function(){
    // summary:
    //  get heading and set as title on button icon if necessary
    if (this.showHeading == false){
      var titleText = "";
      this.heading = this.titleNode.innerHTML;
      titleText = dojo.trim(this.titleNode.innerText || this.titleNode.textContent || '');
      // set title attrib on iconNode
      this.iconNode.title = titleText;
      dojo.addClass(this.titleNode,"dijitDisplayNone");
    }
    dojo.setSelectable(this.focusNode, false);
    this.inherited(arguments);
  },

  onClick: function(/*Event*/ e){
    // summary: user callback for when button is clicked
    //      if type="submit", return true to perform submit
    return true;
  },

  _clicked: function(/*Event*/ e){
    // summary: internal replaceable function for when the button is clicked
  },

  onClickCloseButton: function(/*Event*/ e){
    // summary: user callback for when close button is clicked
    return true;
  },
  
  onClickSourceButton: function(/*Event*/ e){
    // summary: user callback for when source button is clicked
    return true;
  },
  
  setHeading: function(/*String*/ content){
    // summary: reset the heading (text) of the pane; takes an HTML string
    this.titleNode.innerHTML = this.heading = content;
    this._layoutHack();
    if (this.showTitle == false){
      this.iconNode.title = dojo.trim(this.containerNode.innerText || this.containerNode.textContent || '');
    }
  },
  
});
