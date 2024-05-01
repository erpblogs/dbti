/** @odoo-module */

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

import { formatDate } from "@web/core/l10n/dates";
import { SkillsX2ManyField, skillsX2ManyField } from "../../../../../hr_skills/static/src/fields/skills_one2many/skills_one2many";
import {CommonSkillsListRenderer} from "../../../../../hr_skills/static/src/views/skills_list_renderer";

export class ProjectListRenderer extends CommonSkillsListRenderer {
    get groupBy() {
        return 'line_type_id';
    }

    get colspan() {
        if (this.props.activeActions) {
            return 3;
        }
        return 2;
    }

    formatDate(date) {
        return formatDate(date);
    }

    setDefaultColumnWidths() {
    }
}

ProjectListRenderer.template = 'advanced_employee_manager.ProjectListRenderer';
ProjectListRenderer.rowsTemplate = "advanced_employee_manager.ProjectListRenderer.Rows";
ProjectListRenderer.recordRowTemplate = "advanced_employee_manager.ProjectListRenderer.RecordRow";


export class ProjectX2ManyField extends SkillsX2ManyField {
    getWizardTitleName() {
        return _t("Create project");
    }
}

ProjectX2ManyField.components = {
    ...SkillsX2ManyField.components,
    ListRenderer: ProjectListRenderer,
};

export const projectX2ManyField = {
    ...skillsX2ManyField,
    component: ProjectX2ManyField,
};

registry.category("fields").add("project_one2many", projectX2ManyField);
