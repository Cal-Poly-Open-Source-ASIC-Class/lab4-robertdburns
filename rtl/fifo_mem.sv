module fifo_mem #(
    parameter DEPTH = 8,
    parameter DATA_WIDTH = 8,
    parameter PTR_WIDTH = 3
) (
    input  logic                  wclk,
    input  logic                  w_en,
    input  logic                  rclk,
    input  logic                  r_en,
    input  logic [PTR_WIDTH:0]   b_wptr,
    input  logic [PTR_WIDTH:0]   b_rptr,
    input  logic [DATA_WIDTH-1:0] data_in,
    input  logic                  full,
    input  logic                  empty,
    output logic [DATA_WIDTH-1:0] data_out
);

    // FIFO memory array
    logic [DATA_WIDTH-1:0] fifo [0:DEPTH-1];

    // Write logic (write on rising edge of wclk)
    always_ff @(posedge wclk) begin
        if (w_en && !full) begin
            fifo[b_wptr[PTR_WIDTH-1:0]] <= data_in;
        end
    end

    // Read logic (register output on rising edge of rclk)
    always_ff @(posedge rclk) begin
        if (r_en && !empty) begin
            data_out <= fifo[b_rptr[PTR_WIDTH-1:0]];
        end
    end

endmodule
