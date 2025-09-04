#include <Wire.h>

// MODULO QUE PEGA O VOLUME, TRANSFORMA EM PORCENTAGEM E ENVIA PRO ADAU
#define ADAU1701_ADDR 0x34  // endereço exemplo I2C do adau
#define REG_VOLUME    0x0001 // Endereço exemplo do registrador de volume
#define PINO_SOM 34
#define LIMIAR   500

int soundNull(){
    int valor = analogRead(PINO_SOM);   // ADC do ESP32
    return 1 if(valor>LIMIAR) else 0;
}

// Converte porcentagem 0 a 100 para Q5.23 (32 bits)
uint32_t percent_to_Q5_23(float percent) {
    if (percent < 0) percent = 0;
    if (percent > 100) percent = 100;
    float decimal = percent / 100.0f;
    uint32_t q5_23 = (uint32_t)(decimal * (1u << 23));
    return q5_23;
}

// Envia 4 bytes para o adau
void write_to_ADAU(uint16_t reg, uint32_t value) {
    Wire.beginTransmission(ADAU1701_ADDR);

    // Endereço de 16 bits
    Wire.write((reg >> 8) & 0xFF);  // byte alto
    Wire.write(reg & 0xFF);         // byte baixo

    // Valor de 32 bits (MSB primeiro)
    for (int i = 24; i >= 0; i -= 8) {
        Wire.write((value >> i) & 0xFF);
    }
    Wire.endTransmission();
}

void set_sound(float percent) {
    uint32_t qValue = percent_to_Q5_23(percent);
    write_to_ADAU(REG_VOLUME, qValue);
}

void setup() {
    Wire.begin();
    set_sound(50.0f); // exemplo: 50%
}

void loop() {
    // ajuste conforme necessário
}
