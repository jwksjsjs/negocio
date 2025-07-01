#include <Wire.h>  // I2C

#define ADAU1701_ADDR 0x34  // endereço exemplo I2C do adau
#define REG_VOLUME 0x0001   // Endereço exemplo do registrador de volume

// Converte porcentagem 0 a 100 para 32b
uint32_t percentToQ5_23(float percent) {
    if (percent < 0) percent = 0;
    if (percent > 100) percent = 100;

    float decimal = percent / 100.0f;          
    uint32_t q5_23 = decimal * (1 << 23);
    return q5_23;
}

// Envia 4 bytes para o adau
void writeToADAU(uint16_t reg, uint32_t value) {
    Wire.beginTransmission(ADAU1701_ADDR);

    // Enviar endereço de 16 bits
    Wire.write((reg >> 8) & 0xFF);  //byte alto
    Wire.write(reg & 0xFF);          // byte baixo

    // Enviar valor de 32 bits em 4 bytes
    Wire.write((value >> 24) & 0xFF);
    Wire.write((value >> 16) & 0xFF);
    Wire.write((value >> 8) & 0xFF);
    Wire.write(value & 0xFF);

    Wire.endTransmission();
}

void setVolumePercent(float percent) {
    uint32_t qValue = percentToQ5_23(percent);
    writeToADAU(REG_VOLUME, qValue);
}
