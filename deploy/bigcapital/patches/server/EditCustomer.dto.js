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
exports.EditCustomerDto = void 0;
const class_validator_1 = require("class-validator");
const swagger_1 = require("@nestjs/swagger");
const ContactAddress_dto_1 = require("./ContactAddress.dto");
const Validators_1 = require("../../../common/decorators/Validators");
class EditCustomerDto extends ContactAddress_dto_1.ContactAddressDto {
}
exports.EditCustomerDto = EditCustomerDto;
__decorate([
    (0, swagger_1.ApiProperty)({ required: true, description: 'Customer type' }),
    (0, class_validator_1.IsString)(),
    (0, class_validator_1.IsNotEmpty)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "customerType", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Salutation' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "salutation", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'First name' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "firstName", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Last name' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "lastName", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Company name' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "companyName", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: true, description: 'Display name' }),
    (0, class_validator_1.IsString)(),
    (0, class_validator_1.IsNotEmpty)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "displayName", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Website' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "website", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Email' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsEmail)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "email", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Work phone' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "workPhone", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Personal phone' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "personalPhone", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Note' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "note", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Active status' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsBoolean)(),
    __metadata("design:type", Boolean)
], EditCustomerDto.prototype, "active", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Customer code' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "code", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "vatTin", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "areaName", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "areaQq", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], EditCustomerDto.prototype, "creditCategory", void 0);
//# sourceMappingURL=EditCustomer.dto.js.map