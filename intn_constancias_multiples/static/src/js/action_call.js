odoo.define('constancias_multiples.action_button', function (require) {
"use strict";
var core = require('web.core');
var ListController = require('web.ListController');
var FormController = require('web.FormController');
var rpc = require('web.rpc');
var session = require('web.session');
var _t = core._t;
var AbstractField = require('web.AbstractField');
ListController.include({
   renderButtons: function($node) {
   this._super.apply(this, arguments);
       if (this.$buttons) {
         this.$buttons.find('.oe_action_button').click(this.proxy('action_def')) ;
       }
   },
   action_def: function () {
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            name: _t("Selecciona tipo de Constancia"),
            type: 'ir.actions.act_window',
            res_model: 'tipo.constancias.wizard',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new'
        }, options)
    },
    });

FormController.include({
   renderButtons: function($node) {
   this._super.apply(this, arguments);
       if (this.$buttons) {
         this.$buttons.find('.oe_action_button').click(this.proxy('action_def')) ;
       }
   },
   action_def: function () {
        var options = {
            on_reverse_breadcrumb: this.on_reverse_breadcrumb,
        };
        this.do_action({
            name: _t("Selecciona tipo de Constancia"),
            type: 'ir.actions.act_window',
            res_model: 'tipo.constancias.wizard',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new'
        }, options)
    },
    });

//    var FormRenderer = require('web.FormRenderer');
//    FormRenderer.include({
//    autofocus: function () {
//        var record = this.model.get(this.handle, {raw: true});
//        print(record);
//        var self = this;
//        if(self.state.model === 'constancias.multiples'){
//         this._rpc({
//                model: 'constancias.multiples',
//                method: 'getFields',
//                args: [1],
//            }).then(function (result) {
//                console.log(result);
//
//                 var boxes = window.$('.o_invisible_modifier');
//                  for (var x = 0; x < boxes.length; x++) {
//                    var obj = boxes[x];
//                    if (obj.name){
////                        obj.remove();
//                    }
////                    console.log(obj);
//                  }
//        //                var nodes = window.$('.o_invisible_modifier');
//        //                console.log(nodes);
//        //                nodes.remove();
//
//            });
//            }
//        return this._super();
//    },
//});

    });

