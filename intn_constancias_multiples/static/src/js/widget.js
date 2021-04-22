odoo.define('intn_constancias_multiples.field_widget', function (require) {
"use strict";

var BasicFields= require('web.basic_fields');
var FormController = require('web.FormController');
var utils = require('web.utils');
var session = require('web.session');
var field_utils = require('web.field_utils');

var AbstractField = require('web.AbstractField');
var core = require('web.core');
var fieldRegistry = require('web.field_registry');
var AbstractAction = require('web.AbstractAction');
var ActionManager = require('web.ActionManager');


var _t = core._t;
var QWeb = core.qweb;

var FieldVideoPreview = AbstractField.extend({
    className: '-block o_field_video_preview',

    _render: function () {
        var params = this.value;
        var id = this.value;
        this._rpc({
            model: 'constancias.multiples',
            method: 'getFields',
            args: [id,params]
        }).then(function (result) {
            if (result){
            var boxes = window.$('.o_invisible_modifier');
                  for (var x = 0; x < boxes.length; x++) {
                    var obj = boxes[x];
                    var name = obj.getAttribute('name');
                    var text = boxes.eq(x).html();
                    if (result.includes(name) || result.includes(text)){
                        $(obj).removeClass('o_invisible_modifier');
                    }
                  }
            }
        });

        this.$el.html(QWeb.render('productVideo', {
            embedCode: this.value,
        }));
    },

});
fieldRegistry.add('video_preview', FieldVideoPreview);
return FieldVideoPreview;
});