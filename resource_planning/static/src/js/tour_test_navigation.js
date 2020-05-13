odoo.define('resource_planning.tour_test_navigation', function(require) {
    "use strict";
    
    var core = require('web.core');
    var tour = require('web_tour.tour');
    
    var _t = core._t;
    
    var options = {
        test: true,
   		url: "/web",
	};
    
    tour.register('tour_test_navigation', options, [tour.STEPS.SHOW_APPS_MENU_ITEM,
        {
            trigger: '.o_app[data-menu-xmlid="resource_planning.menu_resource"]',
            content: _t('hello this is a test'),
            position: 'bottom'
        }, {
            trigger: '.o_list_button_add',
            content: _t('create a new resource'),
            position: 'bottom'
        }, {
            trigger: 'select[name="project"]',
            content: _t('choose a project'),
            run: 'text Office Design',
            position: 'right'
        }, {
            trigger: 'select[name="employee"]',
            content: _t('choose a employee'),
            run: 'text Mitchell Admin',
            position: 'right'
        }, {
            trigger: 'input[name="base_workload"]',
            content: _t('set workload.'),
            run: 'text 100',
            position: 'right',
        }, {
            trigger: 'input[name="start_date"]',
            content: _t('choose start_date.'),
            run: 'text 2020-04-05 13:42:07',
            position: 'right',
        }, {
            trigger: '.fa-check',
            content: _t('Close Picker'),
            position: 'bottom'
        }, {
            trigger: 'input[name="end_date"]',
            content: _t('choose end_date.'),
            run: 'text 2020-07-05 13:42:07',
            position: 'right',
        }, {
            trigger: '.fa-check',
            content: _t('Close Picker'),
            position: 'bottom'
        }, {
            trigger: '.o_form_button_save',
            content: _t('Save the resource'),
            position: 'bottom'
        }, {
            trigger: '.dropdown-toggle[data-menu-xmlid="resource_planning.menu_weekly"]',
            content: _t('Open the Overview'),
            position: 'bottom'
        }, {
            trigger: '.o_menu_entry_lvl_2[data-menu-xmlid="resource_planning.menu_weekly_employee"]',
            content: _t('Open the Overview'),
            position: 'bottom'
        }, {
            trigger: '.dropdown-toggle',
            content: _t('Open the Overview'),
            position: 'bottom'
        },
    ])
});