package com.endeshaw.erp.controller;

import com.endeshaw.erp.model.Product;
import com.endeshaw.erp.repository.ProductRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/products")
public class ProductController {

    private final ProductRepository repo;

    public ProductController(ProductRepository repo) {
        this.repo = repo;
    }

    // ✅ READ all products
    @GetMapping
    public ResponseEntity<List<Product>> getAllProducts() {
        List<Product> products = repo.findAll();
        if (products.isEmpty()) {
            return ResponseEntity.noContent().build();   // clearer response when empty
        }
        return ResponseEntity.ok(products);
    }

    // ✅ CREATE a new product
    @PostMapping
    public ResponseEntity<Product> addProduct(@RequestBody Product product) {
        Product saved = repo.save(product);
        return ResponseEntity.ok(saved);   // return saved product JSON
    }

    // ✅ UPDATE an existing product
    @PutMapping("/{id}")
    public ResponseEntity<Product> updateProduct(@PathVariable Long id, @RequestBody Product product) {
        return repo.findById(id)
                .map(existing -> {
                    existing.setName(product.getName());
                    Product updated = repo.save(existing);
                    return ResponseEntity.ok(updated);   // return updated product JSON
                })
                .orElse(ResponseEntity.notFound().build());
    }

    // ✅ DELETE a product
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteProduct(@PathVariable Long id) {
        if (repo.existsById(id)) {
            repo.deleteById(id);
            return ResponseEntity.ok("Product deleted successfully"); // return confirmation message
        }
        return ResponseEntity.notFound().build();
    }
}
