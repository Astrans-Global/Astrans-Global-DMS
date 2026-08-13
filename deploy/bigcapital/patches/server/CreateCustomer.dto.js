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
exports.CreateCustomerDto = void 0;
const class_validator_1 = require("class-validator");
const swagger_1 = require("@nestjs/swagger");
const Validators_1 = require("../../../common/decorators/Validators");
const ContactAddress_dto_1 = require("./ContactAddress.dto");
class CreateCustomerDto extends ContactAddress_dto_1.ContactAddressDto {
}
exports.CreateCustomerDto = CreateCustomerDto;
__decorate([
    (0, swagger_1.ApiProperty)({
        required: true,
        description: 'Customer type',
        example: 'business',
    }),
    (0, class_validator_1.IsString)(),
    (0, class_validator_1.IsNotEmpty)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "customerType", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: true,
        description: 'Currency code',
        example: 'USD',
    }),
    (0, class_validator_1.IsString)(),
    (0, class_validator_1.IsNotEmpty)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "currencyCode", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Opening balance',
        example: 5000.0,
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsNumber)(),
    (0, Validators_1.ToNumber)(),
    __metadata("design:type", Number)
], CreateCustomerDto.prototype, "openingBalance", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Opening balance date (required when openingBalance is provided)',
        example: '2024-01-01',
    }),
    (0, class_validator_1.ValidateIf)((o) => o.openingBalance != null),
    (0, class_validator_1.IsNotEmpty)({
        message: 'openingBalanceAt is required when openingBalance is provided',
    }),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "openingBalanceAt", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Opening balance exchange rate',
        example: 1.0,
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsNumber)(),
    (0, Validators_1.ToNumber)(),
    __metadata("design:type", Number)
], CreateCustomerDto.prototype, "openingBalanceExchangeRate", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Opening balance branch ID',
        example: 101,
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsNumber)(),
    (0, Validators_1.ToNumber)(),
    __metadata("design:type", Number)
], CreateCustomerDto.prototype, "openingBalanceBranchId", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Salutation',
        example: 'Mr.',
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "salutation", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'First name',
        example: 'John',
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "firstName", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Last name',
        example: 'Smith',
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "lastName", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Company name',
        example: 'Acme Corporation',
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "companyName", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: true,
        description: 'Display name',
        example: 'Acme Corporation',
    }),
    (0, class_validator_1.IsString)(),
    (0, class_validator_1.IsNotEmpty)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "displayName", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Website',
        example: 'https://www.acmecorp.com',
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "website", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Email',
        example: 'contact@acmecorp.com',
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsEmail)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "email", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Work phone',
        example: '+1 (555) 123-4567',
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "workPhone", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Personal phone' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "personalPhone", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Note' }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "note", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({ required: false, description: 'Active status', default: true }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsBoolean)(),
    __metadata("design:type", Boolean)
], CreateCustomerDto.prototype, "active", void 0);
__decorate([
    (0, swagger_1.ApiProperty)({
        required: false,
        description: 'Customer code',
        example: 'CUST-001',
    }),
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "code", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "vatTin", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "areaName", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "areaQq", void 0);
__decorate([
    (0, Validators_1.IsOptional)(),
    (0, class_validator_1.IsString)(),
    __metadata("design:type", String)
], CreateCustomerDto.prototype, "creditCategory", void 0);
//# sourceMappingURL=CreateCustomer.dto.js.map