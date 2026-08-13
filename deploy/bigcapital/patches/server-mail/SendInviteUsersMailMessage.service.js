"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.SendInviteUsersMailMessage = void 0;
const path = require("path");
const common_1 = require("@nestjs/common");
const config_1 = require("@nestjs/config");
const Mail_1 = require("../../Mail/Mail");
const MailTransporter_service_1 = require("../../Mail/MailTransporter.service");
const TenancyContext_service_1 = require("../../Tenancy/TenancyContext.service");
let SendInviteUsersMailMessage = class SendInviteUsersMailMessage {
    constructor(mailTransporter, tenancyContext, configService) {
        this.mailTransporter = mailTransporter;
        this.tenancyContext = tenancyContext;
        this.configService = configService;
    }
    async sendInviteMail(fromUser, invite) {
        const tenant = await this.tenancyContext.getTenant(true);
        const root = path.join(global.__images_dirname, '/bigcapital.png');
        const baseURL = this.configService.get('app.baseUrl');
        const mail = new Mail_1.Mail()
            .setSubject(`${fromUser.firstName} has invited you to join Astrans Books`)
            .setView('mail/UserInvite.html')
            .setTo(invite.email)
            .setAttachments([
            {
                filename: 'bigcapital.png',
                path: root,
                cid: 'bigcapital_logo',
            },
        ])
            .setData({
            root,
            acceptUrl: `${baseURL}/auth/invite/${invite.token}/accept`,
            fullName: `${fromUser.firstName} ${fromUser.lastName}`,
            firstName: fromUser.firstName,
            lastName: fromUser.lastName,
            email: fromUser.email,
            organizationName: tenant.metadata.name,
        });
        this.mailTransporter.send(mail);
    }
};
exports.SendInviteUsersMailMessage = SendInviteUsersMailMessage;
exports.SendInviteUsersMailMessage = SendInviteUsersMailMessage = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [MailTransporter_service_1.MailTransporter,
        TenancyContext_service_1.TenancyContext,
        config_1.ConfigService])
], SendInviteUsersMailMessage);
//# sourceMappingURL=SendInviteUsersMailMessage.service.js.map