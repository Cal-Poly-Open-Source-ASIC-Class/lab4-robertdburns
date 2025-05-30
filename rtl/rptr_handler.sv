module rptr_handler #(
    parameter PTR_WIDTH = 3
) (
    input  logic                rclk,
    input  logic                rrst_n,
    input  logic                r_en,
    input  logic [PTR_WIDTH:0] g_wptr_sync,
    output logic [PTR_WIDTH:0] b_rptr,
    output logic [PTR_WIDTH:0] g_rptr,
    output logic               empty
);

    logic [PTR_WIDTH:0] b_rptr_next;
    logic [PTR_WIDTH:0] g_rptr_next;
    logic               rempty;

    // Update binary and gray pointers synchronously
    always_ff @(posedge rclk or negedge rrst_n) begin
        if (!rrst_n) begin
            b_rptr <= 0;
            g_rptr <= 0;
        end else if (r_en && !empty) begin
            b_rptr <= b_rptr + 1;
            g_rptr <= (b_rptr + 1) ^ ((b_rptr + 1) >> 1);  // Gray encoding
        end
    end

    // Empty flag logic
    always_ff @(posedge rclk or negedge rrst_n) begin
        if (!rrst_n) begin
            empty <= 1;
        end else begin
            empty <= (g_wptr_sync == g_rptr);
        end
    end

endmodule
