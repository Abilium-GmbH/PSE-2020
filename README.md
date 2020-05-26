Version 0.8
# Odoo Resource-Planning Module 

Resource-Planning is a module for the enterprise-resource-planning (ERP) software [odoo](https://www.odoo.com) - (https://github.com/odoo/odoo).

It consists of 2 modules. The first one is the main module `resource_planning` the second `resource_planning_report` is a extension to the first that add some extended report functionality `

This module allows you to manage the workload of your employees on a weekly basis. Therefore it uses the data of the [Employee](https://www.odoo.com/page/employees)
and the [Project](https://www.odoo.com/page/project-management) module. You only have to enter how the workload (percentage) you want a employee 
to invest in to a project during a time period.

It was developed by 5 Computer Science students at the university of Bern in cooperation with [Abilium](https://www.abilium.com/).

## Getting started

To use this module you have to have odoo installed. You can find a detailed description [here](https://www.odoo.com/documentation/13.0/setup/install.html#id4).
We developed the module for the community edition of odoo. It should work just fine with the Enterprise Edition but wasn't tested by us.

Once odoo is installed you can download and install this module. Therefore you have to copy the contents of our repository in to your addons folder. It is important 
that the folders `resource_planning` and `resource_planning_report` are in the addons folder and not in a subfolder.

Now just open your odoo go to the Apps Page and install the resource_planning module. This will automatically install the Employee and Project modules if they arn't
allready installed. Once `resource_planning` is installed you can install `resource_planning_report`. Be aware that you'll have to delete the `Apps` filter on the Apps-Page in order to see
the report module.

## Documentation
tbd
