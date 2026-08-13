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
exports.AuthenticationMailMesssages = void 0;
const common_1 = require("@nestjs/common");
const path = require("path");
const config_1 = require("@nestjs/config");
const Mail_1 = require("../Mail/Mail");
const MailTransporter_service_1 = require("../Mail/MailTransporter.service");
let AuthenticationMailMesssages = class AuthenticationMailMesssages {
    constructor(configService, mailTransporter) {
        this.configService = configService;
        this.mailTransporter = mailTransporter;
    }
    resetPasswordMessage(user, token) {
        const baseURL = this.configService.get('app.baseUrl');
        return new Mail_1.Mail()
            .setSubject('Astrans Books - Password Reset')
            .setView('mail/ResetPassword.html')
            .setTo(user.email)
            .setAttachments([
            {
                filename: 'bigcapital.png',
                path: path.join(global.__static_dirname, `/images/bigcapital.png`),
                cid: 'bigcapital_logo',
            },
        ])
            .setData({
            resetPasswordUrl: `${baseURL}/auth/reset_password/${token}`,
            first_name: user.firstName,
            last_name: user.lastName,
        });
    }
    sendResetPasswordMail(user, token) {
        const mail = this.resetPasswordMessage(user, token);
        return this.mailTransporter.send(mail);
    }
    signupVerificationMail(email, fullName, token) {
        const baseURL = this.configService.get('app.baseUrl');
        const verifyUrl = `${baseURL}/auth/email_confirmation?token=${token}&email=${email}`;
        return new Mail_1.Mail()
            .setSubject('Astrans Books - Verify your email')
            .setView('mail/SignupVerifyEmail.html')
            .setTo(email)
            .setAttachments([
            {
                filename: 'bigcapital.png',
                path: path.join(global.__static_dirname, `/images/bigcapital.png`),
                cid: 'bigcapital_logo',
            },
        ])
            .setData({ verifyUrl, fullName });
    }
    sendSignupVerificationMail(email, fullName, token) {
        const mail = this.signupVerificationMail(email, fullName, token);
        return this.mailTransporter.send(mail);
    }
};
exports.AuthenticationMailMesssages = AuthenticationMailMesssages;
exports.AuthenticationMailMesssages = AuthenticationMailMesssages = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [config_1.ConfigService,
        MailTransporter_service_1.MailTransporter])
], AuthenticationMailMesssages);
//# sourceMappingURL=AuthMailMessages.esrvice.js.map